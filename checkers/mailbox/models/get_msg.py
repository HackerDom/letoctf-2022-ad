from attrs import define, field

from models.default_rsp import DefaultRsp


@define
class GetMsgReq:
    msg_id: bytes
    encryption: bytes = field(default=None)


@define
class GetMsgRsp(DefaultRsp):
    id: bytes
    text: bytes
