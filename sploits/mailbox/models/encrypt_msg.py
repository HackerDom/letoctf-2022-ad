from attrs import define

from models.default_rsp import DefaultRsp


@define
class EncryptMsgReq:
    msg_id: bytes
    user_id: bytes


@define
class EncryptMsgRsp(DefaultRsp):
    msg_id: bytes
    encryption: bytes
