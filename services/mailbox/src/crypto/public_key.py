from random import getrandbits

from crypto.utils import inverse_mod
from model.private_key import PrivateKey


class PublicKey:
    def __init__(self, n:int):
        self._n = n
        self._n_2 = pow(n, 2)

    def as_dict(self):
        return {'n': self._n}

    @staticmethod
    def from_private_key(private_key:PrivateKey):
        return PublicKey(n=private_key._p * private_key._q)

    def encrypt(self, pt:int) -> int:
        r = getrandbits(self._n.bit_length())
        return (pow(self._n + 1, pt, self._n_2) * pow(r, self._n, self._n_2)) % self._n_2
