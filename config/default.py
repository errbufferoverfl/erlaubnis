import os
import secrets

BASEDIR = os.path.abspath(os.path.dirname(__name__))


class Configuration(object):
    """
    The default configuration for this Flask application.
    """

    """
    Project Details
    These are used to pre-fill the Jinja templates.
    """
    TITLE = "Erlaubnis"
    DESCRIPTION = "A not very good OAuth2.1 authorisation server."
    AUTHORS = ["errbufferoverfl", ]
    TAGS = ["development", "security"]
    LANG = "en"

    """Flask Configuration"""
    DEBUG = False
    TESTING = False
    THREADS_PER_PAGE = 8

    """Security Configuration"""
    ADMINS = frozenset()
    SECURITY_PASSWORD_SALT = secrets.token_bytes(128)
    SECRET_KEY = secrets.token_bytes(128)
    SESSION_COOKIE_SAMESITE = "strict"

    """Database Configuration"""
    DATABASE_NAME = "app.db"

    @property
    def SQLALCHEMY_DATABASE_URI(self):  # noqa
        return f"sqlite:///{BASEDIR}/{self.DATABASE_NAME}"

    """API Meta Configuration"""
    API_TITLE = f"{TITLE} - API Reference"
    API_VERSION = "1.0"

    """Open API Configuration"""
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_JSON_PATH = "api-spec.json"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_URL = (
        "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    )
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    OPENAPI_RAPIDOC_PATH = "/rapidoc"
    OPENAPI_RAPIDOC_URL = "https://unpkg.com/rapidoc/dist/rapidoc-min.js"
    OPENAPI_RAPIDOC_CONFIG = {
        "theme": "light",
        "layout": "column",
        "schema-style": "table",
        "schema-hide-read-only": "never",
        "default-schema-tab": "example",
    }
