from crypto.const import HASH_TABLE


class Hash:
    def __init__(self, msg:bytes=None):
        self._index = 0
        self._value = self._process(msg or b'')

    def _process(self, msg:bytes, init_value:int=0x6d61696c626f78):
        init_value ^= 0xffffffffffffffff
        for x in msg:
            init_value = (init_value >> 8) ^ HASH_TABLE[(self._index & 0xff) ^ x]
            self._index += 1
        return init_value ^ 0xffffffffffffffff

    def update(self, msg:bytes):
        self._value = self._process(msg, self._value)
        return self

    def digest(self) -> int:
        return bytes.fromhex(self.hexdigest())

    def hexdigest(self) -> str:
        return hex(self._value)[2:].zfill(16)