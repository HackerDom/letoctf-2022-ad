from base64 import b64encode, b64decode
from typing import Any

from gornilo.http_clients import requests_with_retries

from crypto.private_key import PrivateKey
from crypto.public_key import PublicKey
from models import *


class API:
    def __init__(self, host:str, port:int):
        self._addr = f'http://{host}:{port}'
        self._session = requests_with_retries()

    def ping(self):
        rsp = self._session.get(
            f'{self._addr}/ping'
        ).json()
        return PingRsp(
            status=rsp['status'],
            msg=rsp['response']['msg']
        )

    def register(self, req:RegisterReq) -> RegisterRsp:
        rsp = self._session.post(
            f'{self._addr}/register', 
            json={
                'username': b64encode(req.username).decode(),
                'password': b64encode(req.password).decode()
            }
        ).json()
        return RegisterRsp(
            status=rsp['status'],
            user_id=b64decode(rsp['response']['user_id'].encode())
        )

    def login(self, req: LoginReq) -> LoginRsp:
        rsp = self._session.post(
            f'{self._addr}/login', 
            json={
                'username': b64encode(req.username).decode(),
                'password': b64encode(req.password).decode()
            }
        ).json()
        return LoginRsp(
            status=rsp['status'],
            user_id=b64decode(rsp['response']['user_id'])
        )

    def me(self) -> LoginRsp:
        rsp = self._session.get(
            f'{self._addr}/me'
        ).json()
        user = rsp['response']['user']
        return MeRsp(
            status=rsp['status'],
            user_id=b64decode(user['id'].encode()),
            username=b64decode(user['username'].encode()),
            private_key=PrivateKey(user['private_key']['p'], user['private_key']['q']),
            public_key=PublicKey(user['public_key']['n'])
        )

    def get_user_info(self, req: GetUserInfoReq) -> GetUserInfoRsp:
        rsp = self._session.get(
            f'{self._addr}/get_user_info',
            params={
                'username': b64encode(req.username).decode()
            }
        ).json()
        user = rsp['response']['user']
        return GetUserInfoRsp(
            status=rsp['status'],
            user_id=b64decode(user['id'].encode()),
            username=b64decode(user['username'].encode()),
            public_key=PublicKey(user['public_key']['n'])
        )

    def create_dialogue(self, req:CreateDialogueReq) -> CreateDialogueRsp:
        rsp = self._session.post(
            f'{self._addr}/create_dialogue',
            json={
                'username': b64encode(req.username).decode(),
                'name': b64encode(req.name).decode()
            }
        ).json()
        return CreateDialogueRsp(
            status=rsp['status'],
            id=b64decode(rsp['response']['dialogue']['id'].encode()),
            name=b64decode(rsp['response']['dialogue']['name'].encode())
        )

    def get_dialogue(self, req:GetDialogueReq) -> GetDialogueRsp:
        rsp = self._session.get(
            f'{self._addr}/get_dialogue',
            params={
                'username': b64encode(req.username).decode()
            }
        ).json()
        return CreateDialogueRsp(
            status=rsp['status'],
            id=b64decode(rsp['response']['dialogue']['id'].encode()),
            name=b64decode(rsp['response']['dialogue']['name'].encode())
        )

    def send_msg(self, req:SendMsgReq) -> SendMsgRsp:
        rsp = self._session.post(
            f'{self._addr}/send_msg',
            json={
                'dialogue': b64encode(req.dialogue_id).decode(),
                'text': b64encode(req.text).decode()
            }
        ).json()
        return SendMsgRsp(
            status=rsp['status'],
            id=b64decode(rsp['response']['msg']['id'].encode()),
            encryption=b64decode(rsp['response']['msg']['encryption'].encode()),
            user_from_id=b64decode(rsp['response']['msg']['user_from_id'].encode()),
            user_to_id=b64decode(rsp['response']['msg']['user_to_id'].encode())
        )

    def get_msg(self, req:GetMsgReq) -> GetMsgRsp:
        data = {
            'msg': b64encode(req.msg_id).decode()
        }
        if req.encryption is not None:
            data['encryption'] = b64encode(req.encryption).decode()

        rsp = self._session.get(
            f'{self._addr}/get_msg',
            params=data
        ).json()
        return GetMsgRsp(
            status=rsp['status'],
            id=b64decode(rsp['response']['msg']['id'].encode()),
            text=b64decode(rsp['response']['msg']['text'].encode())
        )
