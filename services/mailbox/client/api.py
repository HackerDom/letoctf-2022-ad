from base64 import b64encode, b64decode
from typing import Any

from requests import Session


class API:
    def __init__(self, host:str, port:int):
        self._addr = f'http://{host}:{port}'
        self._session = Session()

    def register(self, username:bytes, password:bytes) -> dict[str, Any]:
        return self._session.post(
            f'{self._addr}/register', 
            json={
                'username': b64encode(username).decode(),
                'password': b64encode(password).decode()
            }
        ).json()

    def login(self, username:bytes, password:bytes) -> dict[str, Any]:
        return self._session.post(
            f'{self._addr}/login', 
            json={
                'username': b64encode(username).decode(),
                'password': b64encode(password).decode()
            }
        ).json()

    def me(self) -> dict[str, Any]:
        return self._session.get(
            f'{self._addr}/me'
        ).json()

    def get_user_info(self, username:bytes) -> dict[str, Any]:
        return self._session.get(
            f'{self._addr}/get_user_info',
            params={
                'username': b64encode(username).decode()
            }
        ).json()

    def create_dialogue(self, username:bytes, name:bytes) -> dict[str, Any]:
        return self._session.post(
            f'{self._addr}/create_dialogue',
            json={
                'username': b64encode(username).decode(),
                'name': b64encode(name).decode()
            }
        ).json()

    def get_dialogue(self, username:bytes) -> dict[str, Any]:
        return self._session.get(
            f'{self._addr}/get_dialogue',
            params={
                'username': b64encode(username).decode()
            }
        ).json()

    def send_msg(self, dialogue_id:bytes, text:bytes) -> dict[str, Any]:
        return self._session.post(
            f'{self._addr}/send_msg',
            json={
                'dialogue': b64encode(dialogue_id).decode(),
                'text': b64encode(text).decode()
            }
        ).json()

    def get_msg(self, msg_id:bytes, encryption:bytes=None) -> dict[str, Any]:
        data = {
            'msg': b64encode(msg_id).decode()
        }
        if encryption is not None:
            data['encryption'] = b64encode(encryption)

        return self._session.get(
            f'{self._addr}/get_msg',
            params=data
        ).json()