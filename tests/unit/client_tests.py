import pytest

from app.client.models import Client


def test_client_creation(new_user):
    """
    GIVEN a Client model
    WHEN a new Client is created
    THEN check the name, authentication method, and grant types are defined correctly
    """
    client_one = Client("Test Client 1", 0, ["authorization_code", ], new_user.user_id)

    assert client_one.id is not None
    assert client_one.client_name == "Test Client 1"
    assert client_one.token_endpoint_auth_method == 0
    assert client_one.grant_types == "['authorization_code']"
    assert client_one.owner_id == new_user.user_id


def test_client_creation_no_owner():
    """
    GIVEN a Client model
    WHEN a new Client is created without an owner
    THEN raise a TypeError
    """
    with pytest.raises(TypeError) as err:
        client_one = Client("", 0, ["authorization_code", ], )


def test_client_creation_sneaky_no_owner():
    """
    GIVEN a Client model
    WHEN a new Client is created with a blank string, or None in the owner_id
    THEN raise a TypeError
    """
    with pytest.raises(TypeError) as err:
        client_one = Client("", 0, ["authorization_code", ], None)
    assert "Client must have a valid owner associated with it." in str(err.value)

    with pytest.raises(TypeError):
        client_one = Client("", 0, ["authorization_code", ], "")
    assert "Client must have a valid owner associated with it." in str(err.value)


def test_nameless_client_creation(new_user):
    """
    GIVEN a Client model
    WHEN a new Client is created without a client_name
    THEN check the client_id is returned in place of the client_name
    """
    client_one = Client("", 0, ["authorization_code", ], new_user.user_id)

    assert client_one.id is not None
    assert client_one.client_name == client_one.id
