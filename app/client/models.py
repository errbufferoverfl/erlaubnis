import uuid

from sqlalchemy import String, Text, func

from app import db
from app.core.models import BaseModel


class ClientInstallation(db.Model):
    __tablename__ = "client_users"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column("user_id", db.String(), db.ForeignKey("user.fs_uniquifier"))

    client_id = db.Column("client_id", db.String(), db.ForeignKey("client._id"))
    client_secret = db.Column("client_secret", db.String())


class ClientOwner(db.Model):
    __tablename__ = "client_owner"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column("user_id", db.String(), db.ForeignKey("user.fs_uniquifier"))
    client_id = db.Column("client_id", db.String(), db.ForeignKey("client._id"))


class Client(BaseModel):
    __tablename__ = "client"
    _id = db.Column(String(255), unique=True, nullable=False, primary_key=True, index=True)
    _name = db.Column(String(120), nullable=False)

    _is_confidential = db.Column(db.Boolean, nullable=False)

    _client_metadata = db.Column('client_metadata', Text)

    owner_id = db.Column(db.Integer, db.ForeignKey('user.fs_uniquifier'))
    owner = db.relationship("User", back_populates="client")

    # metadata
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=func.now(), nullable=True)

    def __init__(self, user, name):
        self._id = self.generate_id()
        self._name = name
        self.owner = user

        self._is_confidential = True

    @staticmethod
    def generate_id():
        return uuid.uuid4().__str__()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def redirect_uris(self) -> list:
        """
        Client URIs
        [Source](https://www.rfc-editor.org/rfc/rfc6749#section-3.1.2)

        The URI in which the authorization server should redirect the user-agent back to.
        The authorization server SHOULD require all clients to register their redirection endpoint prior to utilizing the
        authorization endpoint.

        The redirection endpoint SHOULD require the use of TLS as described in Section 1.6 when the requested
        response type is "code" or "token".

        Returns:

        """
        return self.client_metadata.get('redirect_uris', [])

    def valid_redirect_uri(self, redirect_uri):
        if redirect_uri in self.redirect_uris:
            return True
        return False

    @property
    def scopes(self):
        return self.client_metadata.get('scopes', [])

    @property
    def allowed_grant_types(self):
        return self.client_metadata.get('allowed_grant_types', [])

    def valid_grant_type(self, grant_type):
        if grant_type in self.grant_type:
            return True
        return False

    @property
    def allowed_response_types(self):
        return self.client_metadata.get('allowed_response_types', [])

    def valid_response_types(self, response_types):
        if response_types in self.response_types:
            return True
        return False
