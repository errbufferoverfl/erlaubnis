from app.client.models import Client


def test_uuid_generations(test_client):
    """
    GIVEN a Client model
    WHEN a new Client is created
    AND a UUID namespace for app_name has been provided
    THEN generate a UUID3 using the provided namespace

    Args:
        test_client:

    Returns:

    """
    client = Client("Test Client 1", "0", ["authorization_code", ])
    assert client.id == "450cd9c7-0c0c-333b-83bb-edd9026e2dc8"

    client_two = Client(" ", "0", ["authorization_code", ])
    assert client_two.id == "1cdf26dd-2934-3d19-8b07-b252cc095655"

    client_three = Client(" ", "0", ["authorization_code", ])
    assert client_two.id != client_three.id
