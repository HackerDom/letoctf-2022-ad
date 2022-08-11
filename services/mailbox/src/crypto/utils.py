from Crypto.Util.number import GCD, bytes_to_long, getPrime, inverse, long_to_bytes


def get_prime(n:int) -> int:
    return getPrime(n)


def inverse_mod(x:int, n:int) -> int:
    return inverse(x, n)


def generate_key(n_bits:int) -> tuple[int, int]:
    while True:
        p = get_prime(n_bits)
        q = get_prime(n_bits)
        if GCD(p*q, (p-1)*(q-1)) != 1:
            continue
        return p, q


def l2b(x:int) -> bytes:
    return long_to_bytes(x)


def b2l(x:bytes) -> int:
    return bytes_to_long(x)
