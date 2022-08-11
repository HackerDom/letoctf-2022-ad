import logging
from base64 import b64encode, b64decode
from typing import Optional

from flask import Response, jsonify, request, session

from app import app
from db import db
from service import Service


service = Service()


def ok_response(**response:dict) -> Response:
    return jsonify(status='ok', response=response)


def error_response(msg:str) -> Response:
    return jsonify(status='error', msg=msg)


def save_user_to_session(user) -> None:
    session['user_id'] = user.id.hex()


def extract_user_from_session():
    hex_user_id = session.get('user_id', None)
    if hex_user_id is None:
        return None, 'login first'
    try:
        user_id = bytes.fromhex(hex_user_id)
    except Exception:
        session.clear()
        return None, 'bad session'

    user = service.get_user_by_user_id(user_id)
    if user is None:
        session.clear()
        return None, 'no such user'

    return user, None


def extract_b64(data:dict, name:str) -> tuple[bytes, str]:
    b64_value = data.get(name, None)
    if b64_value is None:
        return None, f'no {name}'

    try:
        return b64decode(b64_value.encode()), None
    except Exception:
        return None, f'{name} is not in base64'


@app.route('/ping', methods=['GET'])
def ping():
    return ok_response(msg='pong')


@app.route('/register', methods=['POST'])
def register():
    username, error = extract_b64(request.json, 'username')
    if error is not None:
        return error_response(error)

    password, error = extract_b64(request.json, 'password')
    if error is not None:
        return error_response(error)

    user, error = service.register(username, password)
    if error is not None:
        return error_response(error)
    return ok_response(user_id=b64encode(user.id).decode())


@app.route('/login', methods=['POST'])
def login():
    username, error = extract_b64(request.json, 'username')
    if error is not None:
        return error_response(error)

    password, error = extract_b64(request.json, 'password')
    if error is not None:
        return error_response(error)

    user, error = service.login(username, password)
    if error is not None:
        return error_response(error)

    save_user_to_session(user)
    return ok_response(user_id=b64encode(user.id).decode())


@app.route('/me')
def me():
    user, error = extract_user_from_session()
    if error is not None:
        return error_response(error)
    return ok_response(user=service.user_to_json(user, is_private=True))


@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    username, error = extract_b64(request.args, 'username')
    if error is not None:
        return error_response(error)

    user = service.get_user_by_username(username)
    if user is None:
        return error_response('no such user')

    return ok_response(user=service.user_to_json(user, is_private=False))


@app.route('/create_dialogue', methods=['POST'])
def create_dialogue():
    user_from, error = extract_user_from_session()
    if error is not None:
        return error_response(error)

    username, error = extract_b64(request.json, 'username')
    if error is not None:
        return error_response(error)

    user_to = service.get_user_by_username(username)
    if user_to is None:
        return error_response('no such user')

    name, error = extract_b64(request.json, 'name')
    if error is not None:
        return error_response(error)

    dialogue_id = bytes([a^b for a,b in zip(user_from.id, user_to.id)])

    dialogue, error = service.create_dialogue(
        dialogue_id=dialogue_id,
        user_from=user_from, 
        user_to=user_to,
        name=name
    )
    if error is not None:
        return error_response(error)

    return ok_response(dialogue={
        'id': b64encode(dialogue.id).decode(),
        'name': b64encode(dialogue.name).decode()
    })


@app.route('/get_dialogue', methods=['GET'])
def get_dialogue():
    user_from, error = extract_user_from_session()
    if error is not None:
        return error_response(error)

    username, error = extract_b64(request.args, 'username')
    if error is not None:
        return error_response(error)

    user_to = service.get_user_by_username(username)
    if user_to is None:
        return error_response('no such user')

    dialogue_id = bytes([a^b for a,b in zip(user_from.id, user_to.id)])

    dialogue, error = service.get_dialogue_by_id(dialogue_id)
    if error is not None:
        return error_response(error)

    return ok_response(dialogue={
        'id': b64encode(dialogue.id).decode(),
        'name': b64encode(dialogue.name).decode()
    })


@app.route('/send_msg', methods=['POST'])
def send_msg():
    user, error = extract_user_from_session()
    if error is not None:
        return error_response(error)

    dialogue_id, error = extract_b64(request.json, 'dialogue')
    if error is not None:
        return error_response(error)

    dialogue, error = service.get_dialogue_by_id(dialogue_id)
    if error is not None:
        return error_response(error)

    text, error = extract_b64(request.json, 'text')
    if error is not None:
        return error_response(error)

    msg_and_encryption, error = service.send_msg(user, dialogue, text)
    if error is not None:
        return error_response(error)
    msg, encryption = msg_and_encryption

    return ok_response(msg={
        'id': b64encode(msg.id).decode(),
        'encryption': b64encode(encryption).decode(),
        'user_from_id': b64encode(msg.user_from_id).decode(),
        'user_to_id': b64encode(msg.user_to_id).decode()
    })


@app.route('/encrypt_msg', methods=['GET'])
def encrypt_msg():
    msg_id, error = extract_b64(request.args, 'msg_id')
    if error is not None:
        return error_response(error)

    msg = service.get_msg_by_id(msg_id)
    if msg:
        return error_response('cannot encrypt existing msg')

    user_id, error = extract_b64(request.args, 'user_id')
    if error is not None:
        return error_response(error)

    user = service.get_user_by_user_id(user_id)
    if user is None:
        return error_response('no such user')

    encryption = service.encrypt_msg(msg_id, user)

    return ok_response(msg={
        'msg_id': b64encode(msg_id).decode(),
        'encryption': b64encode(encryption).decode()
    })


@app.route('/get_msg', methods=['GET'])
def get_msg():
    user, error = extract_user_from_session()
    if error is not None:
        return error_response(error)

    msg_id, error = extract_b64(request.args, 'msg')
    if error is not None:
        return error_response(error)

    msg = service.get_msg_by_id(msg_id)
    if msg is None:
        return error_response('no such msg')

    if msg.user_to_id != user.id:
        encryption, error = extract_b64(request.args, 'encryption')
        if error is not None:
            return error_response(error)
        if not service.chech_msg_encryption(msg, msg.user_to, encryption):
            return error_response(f'wrong encryption. ask {b64encode(msg.user_to_id).decode()} for right encryption')

    return ok_response(msg={
        'id': b64encode(msg.id).decode(),
        'text': b64encode(msg.text).decode()
    })


if __name__ == '__main__':
    app.run()