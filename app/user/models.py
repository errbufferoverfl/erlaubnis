import datetime as dt
import uuid

import flask_security
from flask_security import UserMixin, RoleMixin
from sqlalchemy import func
from sqlalchemy.orm import relationship, backref

from app import db


class RolesUsers(db.Model):
    __tablename__ = "roles_users"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column("user_id", db.Integer(), db.ForeignKey("user.fs_uniquifier"))
    role_id = db.Column("role_id", db.Integer(), db.ForeignKey("role.id"))


class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    _password = db.Column(db.String(128), nullable=True)

    # trackable details
    last_login_at = db.Column(db.String, default=dt.datetime.utcnow(), nullable=True)
    current_login_at = db.Column(db.String, default=dt.datetime.utcnow(), nullable=True)
    confirmed_at = db.Column(db.String, default=dt.datetime.utcnow(), nullable=True)

    last_login_ip = db.Column(db.String(255), nullable=True)
    current_login_ip = db.Column(db.String(255), nullable=True)
    login_count = db.Column(db.Integer, default=0)

    # metadata
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=func.now(), nullable=True)

    roles = relationship('Role', secondary='roles_users', backref=backref('users', lazy='dynamic'))
    clients = db.relationship('Client', backref='user', lazy=True)

    def __init__(self, username, password, **kwargs):
        """Create instance."""
        self.user_id = self.generate_user_id()
        self.username = username
        self.password = password

    """
    Username
    """

    @staticmethod
    def generate_user_id():
        return uuid.uuid4().__str__()

    @property
    def user_id(self):
        return self.fs_uniquifier

    @user_id.setter
    def user_id(self, uuid: str):  # noqa
        self.fs_uniquifier = uuid

    @user_id.deleter
    def user_id(self):
        raise AttributeError("'id' is not a deletable attribute.")

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, user_password):
        self._password = flask_security.hash_password(user_password)

    @password.deleter
    def password(self):
        raise AttributeError("'password' is not a deletable attribute.")

    def check_password(self, password):
        return flask_security.verify_password(password, self.password)

    @property
    def is_active(self) -> bool:
        return True
