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

    def _build_error_rsp(self, rsp):
        if rsp.get('status') == 'error':
            return ErrorRsp(
                status=rsp['status'],
                msg=rsp['msg']
            )
        return None

    def ping(self):
        rsp = self._session.get(
            f'{self._addr}/ping'
        ).json()
        return self._build_error_rsp(rsp) or PingRsp(
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
        return self._build_error_rsp(rsp) or RegisterRsp(
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
        return self._build_error_rsp(rsp) or LoginRsp(
            status=rsp['status'],
            user_id=b64decode(rsp['response']['user_id'])
        )

    def me(self) -> LoginRsp:
        rsp = self._session.get(
            f'{self._addr}/me'
        ).json()
        return self._build_error_rsp(rsp) or MeRsp(
            status=rsp['status'],
            user_id=b64decode(rsp['response']['user']['id'].encode()),
            username=b64decode(rsp['response']['user']['username'].encode()),
            private_key=PrivateKey(rsp['response']['user']['private_key']['p'], rsp['response']['user']['private_key']['q']),
            public_key=PublicKey(rsp['response']['user']['public_key']['n'])
        )

    def get_user_info(self, req: GetUserInfoReq) -> GetUserInfoRsp:
        rsp = self._session.get(
            f'{self._addr}/get_user_info',
            params={
                'username': b64encode(req.username).decode()
            }
        ).json()
        return self._build_error_rsp(rsp) or GetUserInfoRsp(
            status=rsp['status'],
            user_id=b64decode(rsp['response']['user']['id'].encode()),
            username=b64decode(rsp['response']['user']['username'].encode())
        )

    def create_dialogue(self, req:CreateDialogueReq) -> CreateDialogueRsp:
        rsp = self._session.post(
            f'{self._addr}/create_dialogue',
            json={
                'username': b64encode(req.username).decode(),
                'name': b64encode(req.name).decode()
            }
        ).json()
        return self._build_error_rsp(rsp) or CreateDialogueRsp(
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
        return self._build_error_rsp(rsp) or CreateDialogueRsp(
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
        return self._build_error_rsp(rsp) or SendMsgRsp(
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
        return self._build_error_rsp(rsp) or GetMsgRsp(
            status=rsp['status'],
            id=b64decode(rsp['response']['msg']['id'].encode()),
            text=b64decode(rsp['response']['msg']['text'].encode())
        )
