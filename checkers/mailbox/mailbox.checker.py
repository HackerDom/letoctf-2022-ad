#!/usr/bin/env python3

from typing import Optional
from os import urandom

from gornilo import NewChecker, CheckRequest, GetRequest, PutRequest, Verdict

from api import API
from crypto.hash import Hash
from models import *


checker = NewChecker()
PORT = 3131


def request_wrapper(request, *args) -> tuple[Optional[DefaultRsp], Optional[Verdict]]:
    try:
        rsp = request(*args)
    except Exception as ex:
        print(ex)
        return None, Verdict.DOWN('serivice is down')

    status = rsp.status
    if status == 'error':
        return None, Verdict.MUMBLE(rsp.get('msg', 'no msg from server'))
    if status == 'ok':
        return rsp, None
    return None, Verdict.MUMBLE('wrong status')


def generate_user():
    username = urandom(8)
    password = urandom(8)
    return username, password


def generate_dialogue_name():
    return urandom(8)


def ping(api:API) -> Optional[Verdict]:
    ping_rsp, verdict = request_wrapper(api.ping)
    if verdict is not None:
        return verdict
    if ping_rsp.msg != 'pong':
        return Verdict.MUMBLE('need pong')


def register(api:API, username:bytes, password:bytes) -> Optional[Verdict]:
    register_rsp, verdict = request_wrapper(api.register, RegisterReq(
        username=username, 
        password=password
    ))
    if verdict is not None:
        return verdict
    if Hash(username).digest() != register_rsp.user_id:
        return Verdict.MUMBLE('wrong user id after registration')


def login(api:API, username:bytes, password:bytes) -> Optional[Verdict]:
    login_rsp, verdict = request_wrapper(api.login, LoginReq(
        username=username, 
        password=password
    ))
    if verdict is not None:
        return verdict
    if Hash(username).digest() != login_rsp.user_id:
        return Verdict.MUMBLE('wrong user id after login')


def me(api:API, username:bytes) -> Optional[Verdict]:
    me_rsp, verdict = request_wrapper(api.me)
    if verdict is not None:
        return verdict
    if username != me_rsp.username:
        return Verdict.MUMBLE('wrong username')
    if Hash(username).digest() != me_rsp.user_id:
        return Verdict.MUMBLE('wrong user id')


def register_and_login(api:API, username:bytes, password:bytes) -> Optional[Verdict]:
    if verdict := register(api, username, password):
        return verdict

    if verdict := login(api, username, password):
        return verdict

    if verdict:= me(api, username):
        return verdict


def get_user_info(api:API, username:bytes) -> Optional[Verdict]:
    get_user_info_rsp, verdict = request_wrapper(api.get_user_info, GetUserInfoReq(
        username=username
    ))
    if verdict is not None:
        return verdict
    if username != get_user_info_rsp.username:
        return Verdict.MUMBLE('wrong username')
    if Hash(username).digest() != get_user_info_rsp.user_id:
        return Verdict.MUMBLE('wrong user id')


def create_dialogue(api:API, username:bytes, dialogue_name:bytes) -> Optional[Verdict]:
    create_dialogue_rsp, verdict = request_wrapper(api.create_dialogue, CreateDialogueReq(
        username=username,
        name=dialogue_name
    ))
    if verdict is not None:
        return verdict
    if dialogue_name != create_dialogue_rsp.name:
        return Verdict.MUMBLE('dialogue name was changed')


def get_dialogue(api:API, username:bytes, dialogue_name:bytes) -> tuple[bytes, Optional[Verdict]]:
    get_dialogue_req, verdict = request_wrapper(api.get_dialogue, GetDialogueReq(
        username=username
    ))
    if verdict is not None:
        return None, verdict
    if dialogue_name != get_dialogue_req.name:
        return None, Verdict.MUMBLE('dialogue name was changed')
    return get_dialogue_req.id, None


def send_msg(api:API, dialogue_id:bytes, msg_text:bytes) -> tuple[bytes, Optional[Verdict]]:
    send_msg_rsp, verdict = request_wrapper(api.send_msg, SendMsgReq(
        dialogue_id=dialogue_id,
        text=msg_text
    ))
    if verdict is not None:
        return None, verdict
    return send_msg_rsp.encryption, None


def get_msg(api:API, msg:bytes, msg_encryption:bytes=None) -> Optional[Verdict]:
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
    if verdict := register_and_login(api2, username2, password2):
        return verdict

    if verdict := get_user_info(api1, username2):
        return verdict
    if verdict := get_user_info(api2, username1):
        return verdict

    dialogue_name = generate_dialogue_name()
    if verdict := create_dialogue(api1, username2, dialogue_name):
        return verdict

    dialogue_id, verdict = get_dialogue(api1, username2, dialogue_name)
    if verdict:
        return verdict
    dialogue_id2, verdict = get_dialogue(api2, username1, dialogue_name)
    if verdict:
        return verdict
    if dialogue_id != dialogue_id2:
        return Verdict.MUMBLE('different dialogue ids')

    msg_text = urandom(8)
    msg_encryption, verdict = send_msg(api1, dialogue_id, msg_text)
    if verdict:
        return verdict

    if verdict := get_msg(api1, msg_text, msg_encryption):
        return verdict
    if verdict := get_msg(api2, msg_text):
        return verdict

    return Verdict.OK()


@checker.define_put(vuln_num=1, vuln_rate=1)
def put1(request: PutRequest) -> Verdict:
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
    if verdict := register_and_login(api2, username2, password2):
        return verdict

    dialogue_name = request.flag.encode()
    if verdict := create_dialogue(api1, username2, dialogue_name):
        return verdict

    flag_id = f'{username1.hex()}:{password1.hex()}:{username2.hex()}:{password2.hex()}'
    return Verdict.OK(flag_id)


@checker.define_get(vuln_num=1)
def get1(request: GetRequest) -> Verdict:
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


if __name__ == '__main__':
    checker.run()
