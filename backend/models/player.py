import os

import pyscrypt
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class Player(db.Model):

    __tablename__ = "player"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    notes = db.Column(db.Text)

    def set_password(self, password):
        salt = os.urandom(16)
        self.password_hash = pyscrypt.hash(password.encode('utf-8'), salt, N=16384, r=8, p=1, dkLen=64)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
