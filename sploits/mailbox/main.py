import re
from base64 import b64decode, b64encode
from os import urandom
from random import choice
from string import ascii_letters, digits

from sage.all import factor
from Crypto.Util.number import bytes_to_long, long_to_bytes

from api import API
from models import *
from crypto.const import HASH_TABLE
from crypto.hash import Hash


HOST = '127.0.0.1'
PORT = 3131
ALPHA = ascii_letters + digits
GET_MSG_PATTERN = re.compile(r'wrong encryption\. ask (.+) for right encryption')


def generate_random_string(length:int) -> bytes():
    return ''.join(choice(ALPHA) for _ in range(length)).encode()


def generate_flag() -> bytes:
    return generate_random_string(31) + b'='


def generate_user() -> tuple[bytes, bytes]:
    username = generate_random_string(10)
    password = generate_random_string(10)
    return username, password


def try_hack_hash(h, table, start_index, suffix):
    res = [i for i,x in table if h>>(7*8) == x]
    if not res or start_index < 0:
        yield suffix
    else:
        for x in res:
            yield from try_hack_hash(
                (h ^ HASH_TABLE[x]) << 8, 
                table,
                start_index - 1,
                bytes([x ^ start_index]) + suffix
            )

def crack_login(login_id, table):
    h = int(login_id.hex(), 16)
    h ^= 0xffffffffffffffff

    for x in try_hack_hash(h, table, start_index=7, suffix=b''):
        if len(x) != 8:
            continue
        if Hash(x).hexdigest() == login_id.hex():
            return x


def init_vuln_1(flag):
    username1, password1 = generate_user()
    username2, password2 = generate_user()

    api1 = API(HOST, PORT)
    api1.register(RegisterReq(username=username1, password=password1))
    api1.login(LoginReq(username=username1, password=password1))

    api2 = API(HOST, PORT)
    api2.register(RegisterReq(username=username2, password=password2))
    api2.login(LoginReq(username=username2, password=password2))


    create_dialogue_rsp = api1.create_dialogue(CreateDialogueReq(username=username2, name=flag))
    return create_dialogue_rsp.id


def crack_vuln_1(dialogue_id):
    table = [(i, x >> (7*8)) for i, x in enumerate(HASH_TABLE)]

    login_1 = generate_random_string(8)
    login_id_1 = Hash(login_1).digest()
    login_id_2 = bytes([x^y for x,y in zip(dialogue_id, login_id_1)])

    login_2 = crack_login(login_id_2, table)

    password_1, password_2 = (generate_random_string(10) for _ in '01')

    api1 = API(HOST, PORT)
    api1.register(RegisterReq(username=login_1, password=password_1))
    api1.login(LoginReq(username=login_1, password=password_1))

    api2 = API(HOST, PORT)
    api2.register(RegisterReq(username=login_2, password=password_2))
    api2.login(LoginReq(username=login_2, password=password_2))

    get_dialogue_rsp = api1.get_dialogue(GetDialogueReq(username=login_2))
    return get_dialogue_rsp.name


def init_vuln_2(flag):
    username1, password1 = generate_user()
    username2, password2 = generate_user()

    api1 = API(HOST, PORT)
    api1.register(RegisterReq(username=username1, password=password1))
    api1.login(LoginReq(username=username1, password=password1))

    api2 = API(HOST, PORT)
    api2.register(RegisterReq(username=username2, password=password2))
    api2.login(LoginReq(username=username2, password=password2))


    create_dialogue_rsp = api1.create_dialogue(CreateDialogueReq(username=username2, name=flag))
    send_msg_rsp = api1.send_msg(SendMsgReq(dialogue_id=create_dialogue_rsp.id, text=flag))
    return send_msg_rsp.id


def crack_vuln_2(msg_id):
    api = API(HOST, PORT)
    username, password = urandom(8), urandom(8)
    api.register(RegisterReq(username=username, password=password))
    api.login(LoginReq(username=username, password=password))
    get_msg_rsp = api.get_msg(GetMsgReq(msg_id=msg_id, encryption=b'AAAA'))
    user_id = b64decode(GET_MSG_PATTERN.findall(get_msg_rsp.msg)[0])

    msg_id_int = int(msg_id.hex(), 16)
    min_factor = min(x[0] for x in factor(msg_id_int))
    fake_msg_id = bytes.fromhex(hex(msg_id_int // min_factor)[2:]).zfill(8)

    encrypt_msg_req = api.encrypt_msg(EncryptMsgReq(msg_id=fake_msg_id, user_id=user_id))
    encryption = long_to_bytes(pow(bytes_to_long(encrypt_msg_req.encryption), min_factor))
    return api.get_msg(GetMsgReq(msg_id=msg_id, encryption=encryption)).text


if __name__ == '__main__':
    flag = generate_flag()
    dialogue_id = init_vuln_1(flag)
    print('vuln1 hacked' if crack_vuln_1(dialogue_id) == flag else 'vuln1 not hacked')

    flag = generate_flag()
    msg_id = init_vuln_2(flag)
    print('vuln2 hacked' if crack_vuln_2(msg_id) == flag else 'vuln2 not hacked')
