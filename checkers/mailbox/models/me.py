from attr import define

from crypto.private_key import PrivateKey
from crypto.public_key import PublicKey
from models.default_rsp import DefaultRsp


@define
class MeRsp(DefaultRsp):
    user_id: bytes
    username: bytes
    private_key: PrivateKey
    public_key: PublicKey