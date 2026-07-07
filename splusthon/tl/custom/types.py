# Stub types for Soroush-specific features not yet in the TL schema
from ..tlobject import TLObject


class FactCheck(TLObject):
    CONSTRUCTOR_ID = 0x00000001
    SUBCLASS_OF_ID = 0x00000000

    def __init__(self):
        pass

    def to_dict(self):
        return {'_': 'FactCheck'}

    def _bytes(self):
        return b''

    @classmethod
    def from_reader(cls, reader):
        return cls()


class SuggestedPost(TLObject):
    CONSTRUCTOR_ID = 0x00000002
    SUBCLASS_OF_ID = 0x00000000

    def __init__(self):
        pass

    def to_dict(self):
        return {'_': 'SuggestedPost'}

    def _bytes(self):
        return b''

    @classmethod
    def from_reader(cls, reader):
        return cls()
