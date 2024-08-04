import os

import pyscrypt
from extensions import db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    '''int'''
    name = db.Column(db.String(50), nullable=False)
    '''login for player'''
    email = db.Column(db.String(50), unique=True, nullable=False)
    '''email for player'''
    password_hash = db.Column(db.String(128), nullable=False)
    '''password hash for player'''
    salt = db.Column(db.String(32), nullable=False)
    '''salt for player'''
    notes = db.Column(db.Text)
    '''notes for player'''

    def set_password(self, password):
        '''
        Function to set password.

        :param password: string
        :return: hashed_password: string
        '''
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
        '''
        Function to check password.

        :param password:
        :return: bool: bool
        '''
        hashed_password = pyscrypt.hash(
            password.encode("utf-8"),
            bytes(self.salt, "utf-8"),
            N=16384,
            r=8,
            p=1,
            dkLen=64,
        ).hex()
        return hashed_password == self.password_hash
