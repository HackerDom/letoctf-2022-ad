from os import urandom
from random import getrandbits

from crypto.private_key import PrivateKey
from crypto.public_key import PublicKey
from crypto.utils import b2l, generate_key, inverse_mod, l2b


class Cipher:
    def __init__(self, public_key:PublicKey, private_key:PrivateKey):
        self._public_key = public_key
        self._private_key = private_key

    @staticmethod
    def init(private_key:PrivateKey):
        public_key = PublicKey.from_private_key(private_key)
        return Cipher(private_key, public_key)

    def _l(self, u:int) -> int:
        return (u - 1) // self._n

    def encrypt(self, pt:bytes) -> bytes:
        return l2b(self._public_key.encrypt(b2l(pt)))

    def decrypt(self, ct:bytes) -> bytes:
        return l2b(self._private_key.decrypt(b2l(ct)))
