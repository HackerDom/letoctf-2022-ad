from app import app
from db import db
from model.dialogue import Dialogue
from model.message import Message
from model.private_key import PrivateKey
from model.user import User

db.create_all()