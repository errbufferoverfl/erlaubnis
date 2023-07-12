from sqlalchemy.exc import IntegrityError

import app.user.models
from app import db
from app.client import models


def get(client_id: str, **kwargs):
    client = models.Client.query.filter_by(client_id=client_id).first()
    if not client:
        return None
    else:
        return client


def create(user: app.user.models.User, client_name: str, **kwargs):
    """
    Creates a new client in the database using the provided information.

    Clients should be

    Returns:

    """
    client = models.Client(user, client_name)
    try:
        db.session.add(client)
        db.session.commit()
    except IntegrityError as ie:
        db.session.rollback()
    else:
        return client
