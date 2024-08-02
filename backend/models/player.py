import os

import pyscrypt
from extensions import db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(32), nullable=False)
    notes = db.Column(db.Text)

    def set_password(self, password):
        self.salt = os.urandom(16).hex()  # Generate a new salt
        self.password_hash = pyscrypt.hash(
            password.encode("utf-8"),
            bytes(self.salt, "utf-8"),
            N=16384,
            r=8,
            p=1,
            dkLen=64,
        ).hex()

    def check_password(self, password):
        hashed_password = pyscrypt.hash(
            password.encode("utf-8"),
            bytes(self.salt, "utf-8"),
            N=16384,
            r=8,
            p=1,
            dkLen=64,
        ).hex()
        return hashed_password == self.password_hash
