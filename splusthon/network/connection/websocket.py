import asyncio

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
    """
    def __init__(self, ws):
        self._ws = ws
        self._buffer = bytearray()

    async def readexactly(self, n):
        while len(self._buffer) < n:
            try:
                msg = await self._ws.recv()
            except Exception:
                # WebSocket closed — check if buffer has enough
                break
            if isinstance(msg, str):
                msg = msg.encode()
            self._buffer.extend(msg)
        if len(self._buffer) < n:
            raise IOError('WebSocket closed while reading')
        result = bytes(self._buffer[:n])
        self._buffer = self._buffer[n:]
        return result


class WebSocketWriter:
    """
    Adapter that wraps a websockets connection to expose
    the ``write(data)`` / ``drain()`` / ``close()`` interface
    expected by ``Connection``.
    """
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
        self._closed = True

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
                max_size=2 ** 32,
                ping_interval=None,
            ),
            timeout=timeout
        )

        self._reader = WebSocketReader(self._ws)
        self._writer = WebSocketWriter(self._ws)

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
