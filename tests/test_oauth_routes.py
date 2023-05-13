import pytest


def test_authorize(client):
    assert client.get('/authorize').status_code == 200


@pytest.mark.parametrize(('client_id', 'response_type', 'redirect_uri', 'message'), (
        ("", "code", "https://example.com", b"mandatory_parameter_missing"),
        ("", "token", "https://example.com", b"mandatory_parameter_missing"),
        ("A123456", "code", "https://example.com", b""),
        ("A123456", "token", "https://example.com", b""),
        ("A123456", "jibberish", "https://example.com", b"unsupported_response_type"),
        ("A123456", "", "https://example.com", b"mandatory_parameter_missing"),
        ("A123456", "code", "", b"mandatory_parameter_missing"),
        ("A123456", "token", "", b"mandatory_parameter_missing"),
))
def test_request_example(client, client_id, response_type, redirect_uri, message):
    response = client.get(
        "/api/authorize",
        query_string={"client_id": client_id, "response_type": response_type, "redirect_uri": redirect_uri}
    )

    assert message in response.data
