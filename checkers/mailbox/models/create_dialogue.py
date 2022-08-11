from attrs import define

from models.default_rsp import DefaultRsp


@define
class CreateDialogueReq:
    username: bytes
    name: bytes


@define
class CreateDialogueRsp(DefaultRsp):
    id: bytes
    name: bytes