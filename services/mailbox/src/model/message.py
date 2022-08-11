from datetime import datetime

from db import db

from model.user import User
from model.dialogue import Dialogue


class Message(db.Model):
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    id = db.Column(db.LargeBinary(8), primary_key=True)
    text = db.Column(db.LargeBinary(50), nullable=False)

    user_from_id = db.Column(db.LargeBinary(8), db.ForeignKey('user.id'), nullable=False)
    user_from = db.relationship(User, foreign_keys=[user_from_id])

    user_to_id = db.Column(db.LargeBinary(8), db.ForeignKey('user.id'), nullable=False)
    user_to = db.relationship(User, foreign_keys=[user_to_id])

    dialogue_id = db.Column(db.LargeBinary(8), db.ForeignKey('dialogue.id'), nullable=False)
    dialogue = db.relationship(Dialogue, foreign_keys=[dialogue_id])
