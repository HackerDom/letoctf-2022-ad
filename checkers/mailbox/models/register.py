from attrs import define

from models.default_rsp import DefaultRsp


@define
class RegisterReq:
    username: bytes
    password: bytes


@define
class RegisterRsp(DefaultRsp):
    user_id: bytes