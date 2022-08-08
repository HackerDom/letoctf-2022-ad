from os import urandom
from string import digits, ascii_letters

from const import HASH_TABLE
from crypto.cipher import Cipher
from crypto.hash import Hash


ALPHA = set((digits + ascii_letters + '=').encode())


def xor_bytes(a, b):
    return bytes([x^y for x,y in zip(a, b)])


def gen_table():
    return [(i, x >> (7*8)) for i, x in enumerate(HASH_TABLE)]


def try_decrypt(h, table):
    h ^= 0xffffffffffffffff
    print(hex(h))
    flag = b''
    index = 7
    for _ in range(8):
        res = [i for i,x in table if h>>(7*8) == x]
        if not res:
            print('DONE', flag)
            return
        flag = bytes([res[0] ^ index]) + flag
        h = (h ^ HASH_TABLE[res[0]]) << 8
        index -= 1
        print(hex(h), flag)
    return flag


if __name__ == '__main__':
    table = gen_table()
    print(len(set(x[1] for x in table)))

    cipher = Cipher.init()

    h = Hash(b'ALPHABETA').calculate()
    print(hex(h))
    ct = cipher.encrypt(h)
    try_decrypt(h, table)
    h0 = Hash(urandom(8)).calculate()
    print()
    print(h - h0)
    print()
    hack = try_decrypt(h - h0, table)

    h1 = Hash(hack).calculate()

    ct0 = cipher.encrypt(h0)
    ct1 = cipher.encrypt(h1)

    print(cipher.decrypt((ct0 + ct1) % cipher.n))

    # h1 = Hash(b'ETAGAMM\0').calculate()
    # h2 = Hash(b'\0'*7 + b'A').calculate()

    # print(h == h0^h1^h2)
    # print(Hash(b'123').calculate() == Hash(b'1').update(b'2').update(b'3').calculate())