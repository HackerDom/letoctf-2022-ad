from db import db

from model.private_key import PrivateKey


class User(db.Model):
    id = db.Column(db.LargeBinary(8), primary_key=True)
    username = db.Column(db.LargeBinary(8), nullable=False)
    password_hash = db.Column(db.LargeBinary(8), nullable=False)
    private_key_id = db.Column(db.LargeBinary(8), db.ForeignKey('private_key.id'), nullable=False)
    private_key = db.relationship(PrivateKey)
