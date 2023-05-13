from flask_security import login_user
from sqlalchemy.exc import IntegrityError

from app import db
from app.core.exceptions import UserInputError, UserAlreadyExists
from app.user import models
from app.user.models import User


def login(username: str, password: str) -> models.User:
    """
    Checks the database for the provided username, if it exists checks that the provided password
    matches the registered password hash. Otherwise, returns an empty user.
    Args:
        username (str): the authenticating users unique identifier.
        password (str): the authenticating users unhashed password.

    Returns:
        user (models.User)
    """
    user = User.query.filter_by(username=username).first()
    if user is not None and user.check_password(password):
        login_user(user)
        return user
    else:
        return User()


def create(username: str, password: str) -> models.User:
    """
    Creates a new user in the database using the provided username and password combination.

    Args:
        username (str): the authenticating users unique identifier.
        password (str): the authenticating users unhashed password.

    Raises:
        UserInputError: if username is blank
        UserAlreadyExists: if the username already exists

    Returns:
        user (models.User)
    """
    user = User(username, password)
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as ie:
        db.session.rollback()

        if "NOT NULL constraint failed: user.username" in ie.__str__():
            raise UserInputError(ie.__str__())
        elif "UNIQUE constraint failed" in ie.__str__():
            raise UserAlreadyExists(ie.__str__(),
                                    description=f"Cannot register a new user with username: '{username}'")
    else:
        return user


def delete(user_id: str) -> models.User:
    """
    Deletes an authenticated users account from the database.

    Args:
        user_id (str): the authenticating users unique identifier.

    Returns:
        user (models.User)
    """
    user = User.query.filter_by(fs_uniquifier=user_id).first()
    try:
        db.session.delete(user)
        db.session.commit()
    except IntegrityError as ie:
        db.session.rollback()
    else:
        return user


def get(**kwargs):
    user = None
    if username := kwargs.get("username"):
        user = User.query.filter_by(username=username).first()
    elif user_id := kwargs.get("user_id"):
        user = User.query.filter_by(fs_uniquifier=user_id).first()

    if user:
        return user
    else:
        return None
