import base64
import ipaddress
import struct

from .abstract import Session
from .memory import MemorySession
from ..crypto import AuthKey

_STRUCT_PREFORMAT = '>B{}sH256s'
_STRUCT_PREFORMAT_WITH_LEN = '>BH{}sH256s'

CURRENT_VERSION = '1'


class StringSession(MemorySession):
    """
    This session file can be easily saved and loaded as a string. According
    to the initial design, it contains only the data that is necessary for
    successful connection and authentication, so takeout ID is not stored.

    It is thought to be used where you don't want to create any on-disk
    files but would still like to be able to save and load existing sessions
    by other means.

    You can use custom `encode` and `decode` functions, if present:

    * `encode` definition must be ``def encode(value: bytes) -> str:``.
    * `decode` definition must be ``def decode(value: str) -> bytes:``.
    """
    def __init__(self, string: str = None):
        super().__init__()
        if string:
            if string[0] != CURRENT_VERSION:
                raise ValueError('Not a valid string')

            string = string[1:]
            data = StringSession.decode(string)
            if len(data) == 352:
                # Old format: raw IPv4 bytes
                self._dc_id, ip, self._port, key = struct.unpack(
                    _STRUCT_PREFORMAT.format(4), data)
                self._server_address = ipaddress.ip_address(ip).compressed
            else:
                # New format: length-prefixed address string
                self._dc_id, addr_len, = struct.unpack('>BH', data[:3])
                addr_bytes, self._port, key = struct.unpack(
                    '>{}sH256s'.format(addr_len), data[3:])
                self._server_address = addr_bytes.decode('utf-8')
            if any(key):
                self._auth_key = AuthKey(key)

    @staticmethod
    def encode(x: bytes) -> str:
        return base64.urlsafe_b64encode(x).decode('ascii')

    @staticmethod
    def decode(x: str) -> bytes:
        return base64.urlsafe_b64decode(x)

    def save(self: Session):
        if not self.auth_key:
            return ''

        addr = self.server_address.encode('utf-8')
        return CURRENT_VERSION + StringSession.encode(struct.pack(
            _STRUCT_PREFORMAT_WITH_LEN.format(len(addr)),
            self.dc_id,
            len(addr),
            addr,
            self.port,
            self.auth_key.key
        ))
