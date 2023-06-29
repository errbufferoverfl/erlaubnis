import pytest


def test_authorize(client):
    assert client.get('/authorize').status_code == 200


@pytest.mark.parametrize(('client_id', 'response_type', 'redirect_uri', 'message'), (
        ("", "code", "https://example.com", "mandatory_parameter_missing"),
        ("", "token", "https://example.com", "mandatory_parameter_missing"),
        # ("A123456", "code", "https://example.com", ""),
        # ("A123456", "token", "https://example.com", ""),
        ("A123456", "code", "", "mandatory_parameter_missing"),
        ("A123456", "token", "", "mandatory_parameter_missing"),
))
def test_request_example(client, client_id, response_type, redirect_uri, message):
    response = client.get(
        "/api/authorize",
        query_string={"client_id": client_id, "response_type": response_type, "redirect_uri": redirect_uri}
    )

    error_msg = response.json
    error_msg = error_msg.get("description")

    assert error_msg == message
