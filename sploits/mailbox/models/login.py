from attrs import define

from models.default_rsp import DefaultRsp


@define
class LoginReq:
    username: bytes
    password: bytes


@define
class LoginRsp(DefaultRsp):
    user_id: bytes