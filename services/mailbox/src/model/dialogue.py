from datetime import datetime

from db import db
from model.user import User


class Dialogue(db.Model):
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    id = db.Column(db.LargeBinary(8), primary_key=True)
    name = db.Column(db.LargeBinary(50), nullable=False)

    initiator_id = db.Column(db.LargeBinary(8), db.ForeignKey('user.id'), nullable=False)
    initiator = db.relationship(User, foreign_keys=[initiator_id])

    participant_id = db.Column(db.LargeBinary(8), db.ForeignKey('user.id'), nullable=False)
    participant = db.relationship(User, foreign_keys=[participant_id])
