from attrs import define

from models.default_rsp import DefaultRsp


@define
class SendMsgReq:
    dialogue_id: bytes
    text: bytes


@define
class SendMsgRsp(DefaultRsp):
    id: bytes
    encryption: bytes
    user_from_id: bytes
    user_to_id: bytes
