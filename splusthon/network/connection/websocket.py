import asyncio
import collections
import logging
import socket

try:
    import aiohttp
except ImportError:
    aiohttp = None

_log = logging.getLogger(__name__)

from .tcpabridged import AbridgedPacketCodec
from .connection import ObfuscatedConnection

from ... import helpers
from ...crypto import AESModeCTR

import os


class WebSocketReader:
    """
    Adapter that wraps an aiohttp WebSocket connection to expose
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
                msg = await self._ws.receive()
            except Exception as e:
                _log.debug('WebSocket receive error: %s', e)
                break
            if msg.type in (aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.CLOSING,
                            aiohttp.WSMsgType.CLOSED):
                break
            if msg.type == aiohttp.WSMsgType.ERROR:
                break
            data = msg.data
            if isinstance(data, str):
                data = data.encode()
            self._chunks.append(data)
            self._total_len += len(data)

        # FIX (bug #2): check this BEFORE touching self._chunks[0]. If the
        # socket closed/errored before any data arrived at all, self._chunks
        # is empty and indexing into it raises IndexError instead of the
        # clean IOError callers expect.
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
    Adapter that wraps an aiohttp WebSocket connection to expose
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
            await self._ws.send_bytes(data)

    def close(self):
        pass

    async def wait_closed(self):
        if self._ws is not None:
            try:
                await self._ws.close()
            except Exception as e:
                _log.debug('WebSocket close error during wait_closed: %s', e)


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

    # NOTE on bug #1 (session cache):
    # A class-level cache is inherently unsafe for this purpose: every
    # instance of ConnectionWebSocket (i.e. every logged-in account / every
    # concurrent client in the same process) shares the same aiohttp
    # ClientSession and can silently steal or invalidate each other's
    # connection. It also never gets cleared when a specific instance's
    # WebSocket dies while the session itself is still open, so the next
    # reconnect for a *different* instance with the same (ip, port, proxy)
    # key can hand back a session tied to a dead socket.
    #
    # Fix: make the cache per-instance instead of per-class. Each
    # ConnectionWebSocket now owns its own session, so there is no
    # cross-instance interference, and the "reuse across reconnects"
    # behavior is preserved for the *same* instance reconnecting.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cached_session = None
        self._cached_session_key = None
        self._reconnect_task = None
        self._reconnect_interval = 1800

    async def _connect(self, timeout=None, ssl=None):
        if aiohttp is None:
            raise ImportError(
                'ConnectionWebSocket requires the "aiohttp" package. '
                'Install it with: pip install aiohttp'
            )

        protocol = 'wss' if self._port == 443 else 'ws'
        url = f'{protocol}://{self._ip}:{self._port}/apiws'

        extra_headers = {
            'Origin': 'https://web.splus.ir'
        }

        connect_timeout = aiohttp.ClientTimeout(total=timeout) if timeout else None
        # Reuse cached session if connection parameters haven't changed
        session_key = (self._ip, self._port, self._proxy, getattr(self, '_local_addr', None))

        # FIX (bug #3): track whether we created a brand-new session in this
        # call, independent of whatever ends up in self._cached_session. The
        # old code compared `session is not self._cached_session` *after*
        # already having assigned session -> self._cached_session, so that
        # check could never be true and a freshly created session would leak
        # on any connection error.
        created_new_session = False

        if self._cached_session is not None and self._cached_session_key == session_key:
            session = self._cached_session
        else:
            if self._cached_session is not None:
                try:
                    await asyncio.wait_for(self._cached_session.close(), timeout=5)
                except Exception as e:
                    _log.debug('Error closing cached session: %s', e)
                self._cached_session = None
                self._cached_session_key = None

            session = aiohttp.ClientSession(timeout=connect_timeout)
            created_new_session = True

        try:
            self._ws = await asyncio.wait_for(
                session.ws_connect(
                    url,
                    headers=extra_headers,
                    protocols=["binary"],
                    max_msg_size=2 ** 24,  # 16 MB
                    heartbeat=30,          # 30s WebSocket-level keepalive
                ),
                timeout=timeout
            )
        except Exception as e:
            _log.warning('WebSocket connection failed: %s', e)
            # Only the session we just created here should be closed on
            # failure; a pre-existing cached session may still be healthy
            # and used by a later reconnect attempt.
            if created_new_session:
                await session.close()
            raise

        # Only commit the session to the cache once we know the connection
        # actually succeeded.
        self._cached_session = session
        self._cached_session_key = session_key

        self._session = session
        self._reader = WebSocketReader(self._ws)
        self._writer = WebSocketWriter(self._ws)

        # Optimize underlying socket for low latency
        try:
            transport = None
            writer_obj = getattr(self._ws, '_writer', None)
            if writer_obj is not None:
                transport = getattr(writer_obj, '_transport', None)
            if transport is not None and hasattr(transport, 'get_extra_info'):
                sock = transport.get_extra_info('socket')
                if sock is not None:
                    # Disable Nagle's algorithm for lower latency
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

                    # Enable TCP keepalive to detect dead connections
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

                    # Reduce send/recv buffer sizes for lower memory usage
                    try:
                        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)
                        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
                    except OSError as e:
                        _log.debug('Failed to set socket buffer sizes: %s', e)

                    # Enable TCP Quick ACK on Linux for faster response
                    try:
                        TCP_QUICKACK = 12
                        sock.setsockopt(socket.IPPROTO_TCP, TCP_QUICKACK, 1)
                    except (OSError, AttributeError) as e:
                        _log.debug('Failed to set TCP_QUICKACK: %s', e)
        except Exception as e:
            _log.debug('Failed to optimize socket settings: %s', e)

        self._codec = self.packet_codec(self)
        self._init_conn()
        await self._writer.drain()

        # Start periodic reconnect loop
        self._reconnect_task = asyncio.ensure_future(self._reconnect_loop())

    async def _reconnect_loop(self):
        """Periodically reset the WebSocket connection every N seconds."""
        try:
            while self._connected:
                await asyncio.sleep(self._reconnect_interval)
                if not self._connected:
                    break
                _log.info('Resetting WebSocket connection (every %ds)', self._reconnect_interval)
                try:
                    await self.disconnect()
                except Exception as e:
                    _log.debug('Error during reconnect disconnect: %s', e)
                try:
                    # Reconnect without starting the reconnect loop again
                    await self._connect()
                    self._connected = True
                    loop = helpers.get_running_loop()
                    self._send_task = loop.create_task(self._send_loop())
                    self._recv_task = loop.create_task(self._recv_loop())
                except Exception as e:
                    _log.warning('WebSocket reconnect failed: %s', e)
                    break
        except asyncio.CancelledError:
            pass

    async def disconnect(self):
        if not self._connected:
            return

        self._connected = False

        await helpers._cancel(
            self._log,
            send_task=self._send_task,
            recv_task=self._recv_task,
            reconnect_task=self._reconnect_task
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

        if hasattr(self, '_session') and self._session:
            # Don't close session if it's cached for reuse
            if self._session is not self._cached_session:
                try:
                    await asyncio.wait_for(self._session.close(), timeout=5)
                except Exception as e:
                    _log.debug('Error closing session during disconnect: %s', e)