from db import db


class PrivateKey(db.Model):
    id = db.Column(db.LargeBinary(16), primary_key=True)
    p = db.Column(db.LargeBinary(128), nullable=False)
    q = db.Column(db.LargeBinary(128), nullable=False)
