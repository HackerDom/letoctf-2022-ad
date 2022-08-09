#!/usr/bin/env python3.9

from random import choice
from string import ascii_letters, digits
from typing import Optional

from gornilo import NewChecker, CheckRequest, GetRequest, PutRequest, Verdict, VulnChecker

from api import API
from crypto.cipher import Cipher
from crypto.hash import Hash
from models import *


ALPHA = ascii_letters + digits
PORT = 3131

checker = NewChecker()


def generate_random_string(length:int):
    return ''.join(choice(ALPHA) for _ in range(length)).encode()


def request_wrapper(request, *args):
    try:
        rsp = request(*args)
    except Exception as ex:
        print(ex)
        return None, Verdict.DOWN('serivice is down')

    status = rsp.status
    if status == 'error':
        return None, Verdict.MUMBLE(rsp.msg)
    if status == 'ok':
        return rsp, None
    return None, Verdict.MUMBLE('wrong status')


def generate_user():
    username = generate_random_string(10)
    password = generate_random_string(10)
    return username, password


def generate_dialogue_name():
    return generate_random_string(12)


def ping(api:API):
    ping_rsp, verdict = request_wrapper(api.ping)
    if verdict is not None:
        return verdict
    if ping_rsp.msg != 'pong':
        return Verdict.MUMBLE('need pong')


def register(api:API, username:bytes, password:bytes):
    register_rsp, verdict = request_wrapper(api.register, RegisterReq(
        username=username, 
        password=password
    ))
    if verdict is not None:
        return verdict
    if Hash(username).digest() != register_rsp.user_id:
        return Verdict.MUMBLE('wrong user id after registration')


def login(api:API, username:bytes, password:bytes):
    login_rsp, verdict = request_wrapper(api.login, LoginReq(
        username=username, 
        password=password
    ))
    if verdict is not None:
        return verdict
    if Hash(username).digest() != login_rsp.user_id:
        return Verdict.MUMBLE('wrong user id after login')


def me(api:API, username:bytes):
    me_rsp, verdict = request_wrapper(api.me)
    if verdict is not None:
        return None, verdict
    if username != me_rsp.username:
        return None, Verdict.MUMBLE('wrong username')
    if Hash(username).digest() != me_rsp.user_id:
        return None, Verdict.MUMBLE('wrong user id')
    return me_rsp, None


def register_and_login(api:API, username:bytes, password:bytes):
    if verdict := register(api, username, password):
        return verdict

    if verdict := login(api, username, password):
        return verdict


def get_user_info(api:API, username:bytes):
    get_user_info_rsp, verdict = request_wrapper(api.get_user_info, GetUserInfoReq(
        username=username
    ))
    if verdict is not None:
        return verdict
    if username != get_user_info_rsp.username:
        return Verdict.MUMBLE('wrong username')
    if Hash(username).digest() != get_user_info_rsp.user_id:
        return Verdict.MUMBLE('wrong user id')


def create_dialogue(api:API, username:bytes, dialogue_name:bytes):
    create_dialogue_rsp, verdict = request_wrapper(api.create_dialogue, CreateDialogueReq(
        username=username,
        name=dialogue_name
    ))
    if verdict is not None:
        return None, verdict
    if dialogue_name != create_dialogue_rsp.name:
        return None, Verdict.MUMBLE('dialogue name was changed')
    return create_dialogue_rsp.id, None


def get_dialogue(api:API, username:bytes, dialogue_name:bytes):
    get_dialogue_req, verdict = request_wrapper(api.get_dialogue, GetDialogueReq(
        username=username
    ))
    if verdict is not None:
        return None, verdict
    if dialogue_name != get_dialogue_req.name:
        return None, Verdict.MUMBLE('dialogue name was changed')
    return get_dialogue_req.id, None


def send_msg(api:API, dialogue_id:bytes, msg_text:bytes):
    send_msg_rsp, verdict = request_wrapper(api.send_msg, SendMsgReq(
        dialogue_id=dialogue_id,
        text=msg_text
    ))
    if verdict:
        return None, verdict
    return (send_msg_rsp.id, send_msg_rsp.encryption), None


def encrypt_msg(api:API, msg_id:bytes, user_id:bytes):
    encrypt_msg_rsp, verdict = request_wrapper(api.encrypt_msg, EncryptMsgReq(
        msg_id=msg_id,
        user_id=user_id
    ))
    if verdict:
        return None, verdict
    return encrypt_msg_rsp.encryption, None


def get_msg(api:API, msg:bytes, msg_encryption:bytes=None):
    msg_id = Hash(msg).digest()
    get_msg_rsp, verdict = request_wrapper(api.get_msg, GetMsgReq(
        msg_id=msg_id,
        encryption=msg_encryption
    ))
    if verdict is not None:
        return verdict
    if get_msg_rsp.text != msg:
        return Verdict.MUMBLE('wrong message')


@checker.define_check
def check_service(request:CheckRequest) -> Verdict:
    api1 = API(request.hostname, PORT)
    if verdict := ping(api1):
        return verdict

    api2 = API(request.hostname, PORT)
    if verdict := ping(api2):
        return verdict

    username1, password1 = generate_user()
    username2, password2 = generate_user()

    if verdict := register_and_login(api1, username1, password1):
        return verdict
    user1, verdict = me(api1, username1)
    if verdict:
        return verdict

    if verdict := register_and_login(api2, username2, password2):
        return verdict
    user2, verdict = me(api2, username2)
    if verdict:
        return verdict

    if verdict := get_user_info(api1, username2):
        return verdict
    if verdict := get_user_info(api2, username1):
        return verdict

    dialogue_name = generate_dialogue_name()
    dialogue_id, verdict = create_dialogue(api1, username2, dialogue_name)
    if verdict:
        return verdict

    dialogue_id1, verdict = get_dialogue(api1, username2, dialogue_name)
    if verdict:
        return verdict
    dialogue_id2, verdict = get_dialogue(api2, username1, dialogue_name)
    if verdict:
        return verdict
    if dialogue_id1 != dialogue_id2:
        return Verdict.MUMBLE('different dialogue ids')

    msg_text = generate_random_string(8)
    before_encryption, verdict = encrypt_msg(api1, Hash(msg_text).digest(), Hash(username2).digest())
    if verdict:
        return verdict

    msg, verdict = send_msg(api1, dialogue_id, msg_text)
    if verdict:
        return verdict
    msg_id, msg_encryption = msg

    if verdict := get_msg(api1, msg_text, before_encryption):
        return verdict
    if verdict := get_msg(api2, msg_text, msg_encryption):
        return verdict

    return Verdict.OK()


@checker.define_vuln(flag_id_description='flag_id is dialogue id (hex)', vuln_rate=1)
class DialogueChecker(VulnChecker):
    @staticmethod
    def put(request: PutRequest) -> Verdict:
        api1 = API(request.hostname, PORT)
        if verdict := ping(api1):
            return verdict

        api2 = API(request.hostname, PORT)
        if verdict := ping(api2):
            return verdict

        username1, password1 = generate_user()
        username2, password2 = generate_user()

        if verdict := register_and_login(api1, username1, password1):
            return verdict
        user1, verdict = me(api1, username1)
        if verdict:
            return verdict

        if verdict := register_and_login(api2, username2, password2):
            return verdict
        user2, verdict = me(api2, username2)
        if verdict:
            return verdict

        dialogue_name = request.flag.encode()
        dialogue_id, verdict = create_dialogue(api1, username2, dialogue_name)
        if verdict:
            return verdict

        flag_id = f'{username1.hex()}:{password1.hex()}:{username2.hex()}:{password2.hex()}'
        return Verdict.OK_WITH_FLAG_ID(dialogue_id.hex(), flag_id)


    @staticmethod
    def get(request: GetRequest) -> Verdict:
        username1, password1, username2, password2 = (bytes.fromhex(x) for x in request.flag_id.split(':'))

        api2 = API(request.hostname, PORT)
        if verdict := ping(api2):
            return verdict

        if verdict := login(api2, username2, password2):
            return verdict

        dialogue_id, verdict = get_dialogue(api2, username1, request.flag.encode())
        if verdict:
            return verdict

        return Verdict.OK()


@checker.define_vuln(flag_id_description='flag_id is message id (hex)')
class MessageChecker(VulnChecker):
    @staticmethod
    def put(request: PutRequest) -> Verdict:
        api1 = API(request.hostname, PORT)
        if verdict := ping(api1):
            return verdict

        api2 = API(request.hostname, PORT)
        if verdict := ping(api2):
            return verdict

        username1, password1 = generate_user()
        username2, password2 = generate_user()

        if verdict := register_and_login(api1, username1, password1):
            return verdict
        user1, verdict = me(api1, username1)
        if verdict:
            return verdict

        if verdict := register_and_login(api2, username2, password2):
            return verdict
        user2, verdict = me(api2, username2)
        if verdict:
            return verdict

        dialogue_name = generate_random_string(32)
        dialogue_id, verdict = create_dialogue(api1, username2, dialogue_name)
        if verdict:
            return verdict

        msg_text = request.flag.encode()
        before_encryption, verdict = encrypt_msg(api1, Hash(msg_text).digest(), Hash(username2).digest())
        if verdict:
            return verdict

        msg, verdict = send_msg(api1, dialogue_id, msg_text)
        if verdict:
            return verdict
        msg_id, msg_encryption = msg

        cipher = Cipher(user2.public_key, user2.private_key)
        if cipher.decrypt(msg_encryption) != msg_id:
            return Verdict.MUMBLE('wrong msg encryption')

        flag_id = ':'.join(
            x.hex()
            for x in (
                username1, password1,
                username2, password2,
                dialogue_id, msg_id,
                msg_encryption, before_encryption
            )
        )
        return Verdict.OK_WITH_FLAG_ID(msg_id.hex(), flag_id)

    @staticmethod
    def get(request: GetRequest) -> Verdict:
        (
            username1, password1, 
            username2, password2, 
            dialogue_id, msg_id, 
            msg_encryption, before_encryption
        ) = (bytes.fromhex(x) for x in request.flag_id.split(':'))
        api1 = API(request.hostname, PORT)
        if verdict := ping(api1):
            return verdict
        if verdict := login(api1, username1, password1):
            return verdict

        msg = request.flag.encode()
        if verdict := get_msg(api1, msg, before_encryption):
            return verdict

        api2 = API(request.hostname, PORT)
        if verdict := ping(api2):
            return verdict
        if verdict := login(api2, username2, password2):
            return verdict
        user2, verdict = me(api2, username2)
        if verdict:
            return verdict
        if verdict := get_msg(api2, msg, msg_encryption):
            return verdict

        return Verdict.OK()


if __name__ == '__main__':
    checker.run()
