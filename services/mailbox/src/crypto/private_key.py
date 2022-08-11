from crypto.utils import b2l, generate_key, inverse_mod


class PrivateKey:
    def __init__(self, p:int, q:int):
        self._p = p
        self._q = q
        self._n = p*q
        self._n_2 = pow(self._n, 2)
        self._lam = (p - 1) * (q - 1)
        self._mu = inverse_mod(self._lam, self._n)

    @staticmethod
    def generate(n_bits:int=1024):
        return PrivateKey(*generate_key(n_bits))

    @staticmethod
    def from_model(private_key):
        return PrivateKey(b2l(private_key.p), b2l(private_key.q))
    
    def as_dict(self):
        return {
            'p': self._p,
            'q': self._q
        }

    def _l(self, u:int) -> int:
        return (u - 1) // self._n

    def decrypt(self, ct:int) -> int:
        return (self._l(pow(ct, self._lam, self._n_2)) * self._mu) % self._n
