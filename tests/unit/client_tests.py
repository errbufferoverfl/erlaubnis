from app.client.models import Client


def test_client_creation():
    """
    GIVEN a Client model
    WHEN a new Client is created
    THEN check the name, authentication method, and grant types are defined correctly
    """
    client_one = Client("Test Client 1", 0, ["authorization_code", ])

    assert client_one.id is not None
    assert client_one.client_name == "Test Client 1"
    assert client_one.token_endpoint_auth_method == 0
    assert client_one.grant_types == "['authorization_code']"


def test_nameless_client_creation():
    """
    GIVEN a Client model
    WHEN a new Client is created without a client_name
    THEN check the client_id is returned in place of the client_name
    """
    client_one = Client("", 0, ["authorization_code", ])

    assert client_one.id is not None
    assert client_one.client_name == client_one.id
