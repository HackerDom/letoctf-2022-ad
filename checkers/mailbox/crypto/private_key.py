from crypto.utils import b2l, generate_key, inverse_mod


class PrivateKey:
    def __init__(self, p:int, q:int):
        self._p = p
        self._q = q
        self._n = p*q
        self._n_2 = pow(self._n, 2)
        self._lam = (p - 1) * (q - 1)
        self._mu = inverse_mod(self._lam, self._n)

    def _l(self, u:int) -> int:
        return (u - 1) // self._n

    def decrypt(self, ct:int) -> int:
        return (self._l(pow(ct, self._lam, self._n_2)) * self._mu) % self._n
