import os

_basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfiguration(object):
    DEBUG = False
    TESTING = False

    ADMINS = frozenset(['youremail@yourdomain.com'])
    SECURITY_PASSWORD_SALT = "SuperSecretPasswordSalt"
    SECRET_KEY = 'SecretKeyForSessionSigning'

    UUID3_NAMESPACE = {
        "app_name": "c767329d-3730-4522-b739-e7883a44c64d"
    }

    THREADS_PER_PAGE = 8

    DATABASE = 'app.db'

    DATABASE_PATH = os.path.join(_basedir, DATABASE)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH

    """
    API Meta Configuration
    """
    API_TITLE = "Not a very good OAuth2 server"
    API_VERSION = "1.0"

    """
    Open API Configuration
    """
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


class TestConfiguration(BaseConfiguration):
    TESTING = True

    DATABASE = 'tests.db'
    DATABASE_PATH = os.path.join(_basedir, DATABASE)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # + DATABASE_PATH


class DebugConfiguration(BaseConfiguration):
    DEBUG = True
