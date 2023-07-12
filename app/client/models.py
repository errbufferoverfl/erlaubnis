import logging
import uuid
from datetime import datetime

from flask import current_app

from app import db
from app.core.models import BaseModel


class InstallationRecords(BaseModel):
    __tablename__ = "installation_record"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column("user_id", db.String(), db.ForeignKey("user.fs_uniquifier"))
    client_id = db.Column("client_id", db.String(), db.ForeignKey("client.id"))
    configuration_id = db.Column("configuration_id", db.String(), db.ForeignKey("client_configuration.id"))


class ClientConfiguration(BaseModel):
    """
    When a client is registered it has a configuration created alongside it, this information defines how that specific
    instance of the app works, including which JSON Web Keys it should use for that specific installation of the client,
    and the types of grant that version of the client should be permitted to use.

    See Also:
        - https://datatracker.ietf.org/doc/html/rfc7517
    """
    __tablename__ = "client_configuration"

    id = db.Column(db.Integer, unique=True, primary_key=True, index=True)
    version = db.Column(db.String())
    jwks = db.Column(db.LargeBinary())
    jwks_uri = db.Column(db.String(2048))
    grant_types = db.Column(db.LargeBinary())

    #installations = db.relationship('ClientConfiguration', backref=db.backref('parent', remote_side='ClientConfiguration.id'))

    def __init__(self, version: str, jwks: str, jwks_uri: str, grant_types: list):
        self.version = version
        self.jwks = jwks
        self.jwks_uri = jwks_uri
        self.grant_types = grant_types


class ClientMetadata(BaseModel):
    """
    When a client is registered it has metadata registered alongside it, this is information that help users learn more
    about the client, before registering the metadata the URIs should be validated using the WhatWG definition of a URL.

    See Also:
        - https://www.rfc-editor.org/rfc/rfc6749
        - https://url.spec.whatwg.org/
    """
    __tablename__ = "client_metadata"

    id = db.Column(db.Integer, unique=True, primary_key=True, index=True)
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
    client_uri = db.Column(db.String(2048), nullable=False)

    logo_uri = db.Column(db.String(2048), nullable=True)
    contacts = db.Column(db.LargeBinary(), nullable=False)
    policy_uri = db.Column(db.String(2048), nullable=False)
    tos_uri = db.Column(db.String(2048), nullable=False)

    def __init__(self, logo_uri: str, contacts: list, policy_uri: str, tos_uri: str, client_uri: str):
        self.logo_uri = logo_uri
        self.contacts = str(contacts)
        self.policy_uri = policy_uri
        self.tos_uri = tos_uri
        self.client_uri = client_uri


class Client(BaseModel):
    __tablename__ = "client"

    """
    Client Identifier
    
    The authorization server issues the registered client a client identifier -- a unique string representing the 
    registration information provided by the client.  The client identifier is not a secret; it is exposed to the 
    resource owner and MUST NOT be used alone for client authentication.  The client identifier is unique to the 
    authorization server.
    """
    id = db.Column(db.String(36), unique=True, nullable=False, primary_key=True, index=True)
    """
    Human-readable string name of the client to be presented to the end-user during authorization.
    If omitted during client configuration, the `_id` will be used. 
    """
    _client_name = db.Column(db.String(255), nullable=True)

    """
    String indicator of the requested authentication method for the token endpoint.  Values defined by this 
    specification are:
    *  "none" (0): The client is a public client as defined in OAuth 2.0, and does not have a client secret.
    *  "client_secret_post" (1): The client uses the HTTP POST parameters as defined in OAuth 2.0.
    *  "client_secret_basic" (2): The client uses HTTP Basic as defined in OAuth 2.0.
    """
    token_endpoint_auth_method = db.Column(db.Integer(), nullable=False)

    """
    Array of OAuth 2.0 grant type strings that the client can use at the token endpoint. 
    These grant types are defined as follows:
     *  "authorization_code": The authorization code grant type defined in OAuth 2.0, Section 4.1.
     *  "implicit": The implicit grant type defined in OAuth 2.0, Section 4.2.
     *  "password": The resource owner password credentials grant type defined in OAuth 2.0, Section 4.3.
     *  "client_credentials": The client credentials grant type defined in OAuth 2.0, Section 4.4.
     *  "refresh_token": The refresh token grant type defined in OAuth 2.0, Section 6.
     *  "urn:ietf:params:oauth:grant-type:jwt-bearer": The JWT Bearer Token Grant Type defined in OAuth JWT Bearer Token 
        Profiles [RFC7523].
     *  "urn:ietf:params:oauth:grant-type:saml2-bearer": The SAML 2.0 Bearer Assertion Grant defined in OAuth SAML 2 
        Bearer Token Profiles [RFC7522].
    """
    grant_types = db.Column(db.LargeBinary())
    owner_id = db.Column(db.String, db.ForeignKey('user.fs_uniquifier'), nullable=False)

    def __init__(self, name: str, token_endpoint_auth_method, grant_types: list):
        self.client_name = name
        self.id = self.generate_id()
        self.token_endpoint_auth_method = token_endpoint_auth_method
        self.grant_types = str(grant_types)

    def generate_id(self):
        uuid_namespace = current_app.config.get("UUID3_NAMESPACE", {})
        app_name_namespace = uuid_namespace.get("app_name")
        try:
            app_name_namespace = uuid.UUID(app_name_namespace)
        except TypeError as err:
            logging.critical(err)
        except ValueError as err:
            logging.critical(err)

        try:
            client_id = uuid.uuid3(app_name_namespace, self.client_name).__str__()
        except TypeError:
            client_id = uuid.uuid4().__str__()
        else:
            return client_id

    @property
    def client_name(self):
        if not self._client_name:
            return self.id
        else:
            return self._client_name

    @client_name.setter
    def client_name(self, name):
        self._client_name = name
