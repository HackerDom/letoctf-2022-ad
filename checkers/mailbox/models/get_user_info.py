from attrs import define

from crypto.public_key import PublicKey
from models.default_rsp import DefaultRsp


@define
class GetUserInfoReq:
    username: bytes


@define
class GetUserInfoRsp(DefaultRsp):
    user_id: bytes
    username: bytes