from attr import define

from models.default_rsp import DefaultRsp


@define
class PingRsp(DefaultRsp):
    msg: str
