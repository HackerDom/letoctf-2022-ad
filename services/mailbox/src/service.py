from base64 import b64encode
from os import urandom
from typing import Any, Optional

from crypto.cipher import Cipher
from crypto.hash import Hash
from crypto.private_key import PrivateKey as CryptoPrivateKey
from crypto.public_key import PublicKey
from crypto.utils import l2b
from db import db
from model.dialogue import Dialogue
from model.message import Message
from model.private_key import PrivateKey as ModelPrivateKey
from model.user import User


ErrorReasonT = Optional[str]
GetUserT = Optional[User]
RegisterT = tuple[Optional[User], ErrorReasonT]
LoginT = tuple[Optional[User], ErrorReasonT]
UserJsonT = dict[str, Any]
DialogueT = tuple[Optional[Dialogue], ErrorReasonT]
MessageT = tuple[Optional[Message], ErrorReasonT]


class Service:
    def _get_cipher_from_user(self, user:User) -> Cipher:
        private_key = CryptoPrivateKey.from_model(user.private_key)
        public_key = PublicKey.from_private_key(private_key)
        return Cipher(public_key, private_key)

    def get_user_by_user_id(self, user_id:bytes) -> GetUserT:
        return User.query.filter_by(id=user_id).first()

    def get_user_by_username(self, username:bytes) -> GetUserT:
        return User.query.filter_by(username=username).first()

    def get_msg_by_id(self, msg_id:bytes) -> MessageT:
        return Message.query.filter_by(id=msg_id).first()

    def register(self, username:bytes, password:bytes) -> RegisterT:
        user_id = Hash(username).digest()
        if self.get_user_by_user_id(user_id) is not None:
            return None, 'user exists'

        crypto_private_key = CryptoPrivateKey.generate()
        model_private_key = ModelPrivateKey(
            id=urandom(16),
            p=l2b(crypto_private_key._p),
            q=l2b(crypto_private_key._q)
        )
        user = User(
            id=user_id,
            username=username,
            password_hash=Hash(password).digest(),
            private_key=model_private_key
        )
        db.session.add(model_private_key)
        db.session.add(user)
        db.session.commit()
        return user, None

    def login(self, username:bytes, password:bytes) -> LoginT:
        user = self.get_user_by_username(username)
        if user is None:
            return None, 'no user'

        if user.password_hash != Hash(password).digest():
            return None, 'wrong password'

        return user, None

    def user_to_json(self, user:User, is_private:False) -> UserJsonT:
        cipher = self._get_cipher_from_user(user)
        res = {
            'id': b64encode(user.id).decode(),
            'username': b64encode(user.username).decode(),
        }
        if is_private:
            res['public_key'] = cipher._public_key.as_dict()
            res['private_key'] = cipher._private_key.as_dict()
        return res

    def create_dialogue(self, dialogue_id:bytes, user_from:User, user_to:User, name:bytes) -> DialogueT:
        if Dialogue.query.filter_by(id=dialogue_id).first() is not None:
            return None, 'dialogue exists'

        dialogue = Dialogue(
            id = dialogue_id,
            name=name,
            initiator=user_from,
            participant=user_to
        )
        db.session.add(dialogue)
        db.session.commit()
        return dialogue, None

    def get_dialogue_by_id(self, dialogue_id:bytes) -> DialogueT:
        dialogue = Dialogue.query.filter_by(id=dialogue_id).first()
        if dialogue is None:
            return None, 'no such dialogue'
        return dialogue, None

    def send_msg(self, user_from:User, dialogue:Dialogue, text:bytes) -> MessageT:
        if user_from.id == dialogue.initiator_id:
            user_to = dialogue.participant
        elif user_from.id == dialogue.participant_id:
            user_to = dialogue.participant
        else:
            return None, 'smthng wrong'

        msg_id = Hash(text).digest()
        if Message.query.filter_by(id=msg_id).first() is not None:
            return None, 'msg exists'

        encryption = self.encrypt_msg(msg_id, user_to)

        msg = Message(
            id=msg_id,
            text=text,
            user_from=user_from,
            user_to=user_to,
            dialogue=dialogue
        )
        db.session.add(msg)
        db.session.commit()
        return (msg, encryption), None
    
    def encrypt_msg(self, msg_id:bytes, user:User) -> bytes:
        cipher = self._get_cipher_from_user(user)
        return cipher.encrypt(msg_id)

    def chech_msg_encryption(self, msg:Message, user:User, encryption:bytes) -> bool:
        cipher = self._get_cipher_from_user(user)
        return cipher.decrypt(encryption) == msg.id