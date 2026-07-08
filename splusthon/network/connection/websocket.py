import asyncio
import collections
import socket

try:
    import websockets
except ImportError:
    websockets = None

from .tcpabridged import AbridgedPacketCodec
from .connection import ObfuscatedConnection

from ...crypto import AESModeCTR

import os


class WebSocketReader:
    """
    Adapter that wraps a websockets connection to expose
    the ``readexactly(n)`` interface expected by ``PacketCodec``.

    Uses a deque of received chunks and memoryview for zero-copy slicing
    to minimize memory allocations under high message rates.
    """
    __slots__ = ('_ws', '_chunks', '_chunk_offset', '_total_len')

    def __init__(self, ws):
        self._ws = ws
        self._chunks = collections.deque()
        self._chunk_offset = 0
        self._total_len = 0

    async def readexactly(self, n):
        while self._total_len < n:
            try:
                msg = await self._ws.recv()
            except Exception:
                break
            if isinstance(msg, str):
                msg = msg.encode()
            self._chunks.append(msg)
            self._total_len += len(msg)

        if self._total_len < n:
            raise IOError('WebSocket closed while reading')

        # Fast path: entire read is within the first chunk
        first = self._chunks[0]
        first_avail = len(first) - self._chunk_offset
        if first_avail >= n:
            result = first[self._chunk_offset:self._chunk_offset + n]
            self._chunk_offset += n
            self._total_len -= n
            if self._chunk_offset >= len(first):
                self._chunks.popleft()
                self._chunk_offset = 0
            return result

        # Slow path: read spans multiple chunks
        # Pre-allocate buffer for known size to avoid list growing
        parts = bytearray(n)
        offset = 0
        remaining = n

        if self._chunk_offset > 0:
            chunk = self._chunks[0]
            avail = len(chunk) - self._chunk_offset
            parts[offset:offset + avail] = memoryview(chunk)[self._chunk_offset:]
            offset += avail
            remaining -= avail
            self._chunks.popleft()
            self._chunk_offset = 0

        while remaining > 0:
            chunk = self._chunks.popleft()
            chunk_len = len(chunk)
            if chunk_len <= remaining:
                parts[offset:offset + chunk_len] = chunk
                offset += chunk_len
                remaining -= chunk_len
            else:
                parts[offset:offset + remaining] = memoryview(chunk)[:remaining]
                self._chunks.appendleft(chunk)
                self._chunk_offset = remaining
                remaining = 0

        self._total_len -= n
        if not self._chunks:
            self._chunk_offset = 0
        return bytes(parts)


class WebSocketWriter:
    """
    Adapter that wraps a websockets connection to expose
    the ``write(data)`` / ``drain()`` / ``close()`` interface
    expected by ``Connection``.

    Buffers pending data in a bytearray and sends in bulk on drain()
    to reduce syscall overhead.
    """
    __slots__ = ('_ws', '_pending')

    def __init__(self, ws):
        self._ws = ws
        self._pending = bytearray()

    def write(self, data):
        self._pending.extend(data)

    async def drain(self):
        if self._pending:
            data = bytes(self._pending)
            self._pending.clear()
            await self._ws.send(data)

    def close(self):
        pass

    async def wait_closed(self):
        if self._ws is not None:
            try:
                await self._ws.close()
            except Exception:
                pass


class WebSocketObfuscatedIO:
    """
    Same obfuscation logic as ``ObfuscatedIO`` in ``tcpobfuscated.py``,
    but works with ``WebSocketReader`` / ``WebSocketWriter`` adapters.
    """
    header = None

    def __init__(self, connection):
        self._reader = connection._reader
        self._writer = connection._writer

        (self.header,
         self._encrypt,
         self._decrypt) = self._init_header(connection.packet_codec)

    @staticmethod
    def _init_header(packet_codec):
        keywords = (b'PVrG', b'GET ', b'POST', b'\xee\xee\xee\xee')
        while True:
            random = os.urandom(64)
            if (random[0] != 0xef and
                    random[:4] not in keywords and
                    random[4:8] != b'\0\0\0\0'):
                break

        random = bytearray(random)
        random_reversed = random[55:7:-1]

        encrypt_key = bytes(random[8:40])
        encrypt_iv = bytes(random[40:56])
        decrypt_key = bytes(random_reversed[:32])
        decrypt_iv = bytes(random_reversed[32:48])

        encryptor = AESModeCTR(encrypt_key, encrypt_iv)
        decryptor = AESModeCTR(decrypt_key, decrypt_iv)

        random[56:60] = packet_codec.obfuscate_tag
        random[56:64] = encryptor.encrypt(bytes(random))[56:64]
        return (random, encryptor, decryptor)

    async def readexactly(self, n):
        return self._decrypt.encrypt(await self._reader.readexactly(n))

    def write(self, data):
        self._writer.write(self._encrypt.encrypt(data))


class ConnectionWebSocket(ObfuscatedConnection):
    """
    WebSocket transport for Soroush messenger.

    Connects to ``wss://{ip}:{port}/apiws`` with Origin header
    set to ``https://web.splus.ir``, then uses obfuscated+abridged
    protocol on top of the WebSocket binary frames.
    """
    obfuscated_io = WebSocketObfuscatedIO
    packet_codec = AbridgedPacketCodec

    async def _connect(self, timeout=None, ssl=None):
        if websockets is None:
            raise ImportError(
                'ConnectionWebSocket requires the "websockets" package. '
                'Install it with: pip install websockets'
            )

        protocol = 'wss' if self._port == 443 else 'ws'
        url = f'{protocol}://{self._ip}:{self._port}/apiws'

        extra_headers = {
            'Origin': 'https://web.splus.ir'
        }

        self._ws = await asyncio.wait_for(
            websockets.connect(
                url,
                additional_headers=extra_headers,
                subprotocols=["binary"],
                max_size=2 ** 24,       # 16 MB - sufficient for Telegram messages
                ping_interval=None,     # MTProto keepalive is used instead
                close_timeout=5,
                max_queue=2 ** 14,      # 16384 - reduced from 65536 to limit memory
                open_timeout=timeout,   # Timeout for connection establishment
            ),
            timeout=timeout
        )

        self._reader = WebSocketReader(self._ws)
        self._writer = WebSocketWriter(self._ws)

        # Optimize underlying socket for low latency
        try:
            transport = self._ws.transport
            if hasattr(transport, 'get_extra_info'):
                sock = transport.get_extra_info('socket')
                if sock is not None:
                    # Disable Nagle's algorithm for lower latency
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

                    # Enable TCP keepalive to detect dead connections
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

                    # Reduce send/recv buffer sizes for lower memory usage
                    # Default is often 128KB+, 64KB is sufficient for MTProto
                    try:
                        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)
                        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
                    except OSError:
                        pass  # Some systems restrict buffer size changes

                    # Enable TCP Quick ACK on Linux for faster response
                    try:
                        TCP_QUICKACK = 12  # Linux-specific
                        sock.setsockopt(socket.IPPROTO_TCP, TCP_QUICKACK, 1)
                    except (OSError, AttributeError):
                        pass  # Not available on all platforms
        except Exception:
            pass

        self._codec = self.packet_codec(self)
        self._init_conn()
        await self._writer.drain()

    async def disconnect(self):
        if not self._connected:
            return

        self._connected = False

        from ... import helpers
        await helpers._cancel(
            self._log,
            send_task=self._send_task,
            recv_task=self._recv_task
        )

        if hasattr(self, '_writer') and self._writer:
            self._writer.close()
            try:
                await asyncio.wait_for(self._writer.wait_closed(), timeout=10)
            except asyncio.TimeoutError:
                self._log.warning(
                    'WebSocket disconnection timed out, forcibly ignoring cleanup'
                )
            except Exception as e:
                self._log.info(
                    '%s during disconnect: %s', type(e), e
                )
