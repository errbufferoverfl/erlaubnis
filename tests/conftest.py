import pytest

from app import create_app
from config import DebugConfiguration


@pytest.fixture()
def app():
    config = DebugConfiguration
    app = create_app(config)
    # other setup can go here

    yield app
    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
