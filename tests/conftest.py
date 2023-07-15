import pytest

from app import create_app, db
from app.client.models import Client
from app.user.models import User
from config import DebugConfiguration


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(DebugConfiguration)

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


@pytest.fixture(scope='module')
def init_database(app):
    # Create the database and the database table
    db.create_all()

    # Insert user data
    default_user = User(username="test_user", password="password")
    second_user = User(username="test_user_two", password="password")
    db.session.add(default_user)
    db.session.add(second_user)

    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()


@pytest.fixture(scope='module')
def new_user(test_client):
    user = User('username@example.com', 'Password1!')
    return user
