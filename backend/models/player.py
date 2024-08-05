import os

import pyscrypt
from backend.extensions import db
from flask_security import UserMixin, RoleMixin


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    played_games = db.Column(db.Integer, unique=False, nullable=False)
    score = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref='players')

    def __init__(self, user_id: int, played_games: int, score: int):
        """Create a new User object using the email address and hashing the
        plaintext password
        """
        self.user_id = user_id
        self.played_games = played_games
        self.score = score


    def __repr__(self):
        return (f'<Player: {self.id}, '
                f'Played games: {self.played_games}, '
                f'User: {self.user_id}>')

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref='roled')
    password_hash = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(32), nullable=False)

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
        return self.password_hash

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

    def __init__(self, name: str, email: str, password: str):
        """Create a new User object using the email address and hashing the
        plaintext password
        """
        self.name = name
        self.email = email
        self.password_hash = self.set_password(password)

    def __repr__(self):
        return (f'<User: {self.id}, '
                f'Password: {self.password_hash}>')


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
