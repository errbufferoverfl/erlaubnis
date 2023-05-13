import uuid

from sqlalchemy import String, Text, func

from app import db
from app.core.models import BaseModel


class ClientUsers(db.Model):
    __tablename__ = "client_users"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column("user_id", db.String(), db.ForeignKey("user.fs_uniquifier"))
    client_id = db.Column("client_id", db.String(), db.ForeignKey("client._id"))


class Client(BaseModel):
    __tablename__ = "client"

    """
    Client Identifier
    
    The authorization server issues the registered client a client identifier -- a unique string representing the 
    registration information provided by the client.  The client identifier is not a secret; it is exposed to the 
    resource owner and MUST NOT be used alone for client authentication.  The client identifier is unique to the 
    authorization server.
    """
    _id = db.Column(String(255), unique=True, nullable=False, primary_key=True, index=True)

    """
    Client Name
    """
    _name = db.Column(String(120))

    _password = db.Column(String(120))
    _is_confidential = db.Column(db.Boolean, nullable=False)
    _is_public = db.Column(db.Boolean, nullable=False)

    _client_metadata = db.Column('client_metadata', Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.fs_uniquifier'))
    owner = db.relationship("User", back_populates="client")

    # metadata
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=func.now(), nullable=True)

    def __init__(self, user, name, **kwargs):
        self._id = self.generate_id()
        self.owner = user
        self._name = name

        self.is_pubic = False
        self.is_confidential = True

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

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def password(self):
        """
        Because we only support confidential clients, we can always support client passwords

        Returns:

        """
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def id(self):
        return self._id

    @property
    def scopes(self):
        return self.client_metadata.get('scopes', [])

    @property
    def allowed_grant_types(self):
        return self.client_metadata.get('allowed_grant_types', [])

    @property
    def allowed_response_types(self):
        return self.client_metadata.get('allowed_response_types', [])

    """
    Client Types
    
    The client type designation is based on the authorization server's definition of secure authentication and its 
    acceptable exposure levels of client credentials. The authorization server SHOULD NOT make assumptions about the 
    client type.
    """

    @property
    def is_pubic(self) -> bool:
        """
        Clients incapable of maintaining the confidentiality of their credentials (e.g., clients executing on the device
        used by the resource owner, such as an installed native application or a web browser-based application), and
        incapable of secure client authentication via any other means.
        """
        return self._is_public

    @is_pubic.setter
    def is_pubic(self, public: bool):
        """
        Args:
            public (bool):

        Returns:

        """
        self._is_public = public

    @property
    def is_confidential(self):
        """
        Clients capable of maintaining the confidentiality of their credentials (e.g., client implemented on a secure server
        with restricted access to the client credentials), or capable of secure client authentication using other means.
        """
        return self._is_confidential

    @is_confidential.setter
    def is_confidential(self, confidential: bool):
        """
        Args:
            confidential (bool):

        Returns:

        """
        self._is_confidential = confidential

    @staticmethod
    def generate_id():
        return uuid.uuid4().__str__()
