from attr import define


@define
class DefaultRsp:
    status: str


@define 
class ErrorRsp(DefaultRsp):
    msg: str