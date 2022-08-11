from attrs import define

from models.default_rsp import DefaultRsp


@define
class GetDialogueReq:
    username: bytes


@define
class GetDialogueRsp(DefaultRsp):
    id: bytes
    name: bytes
