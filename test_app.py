from unittest.mock import patch, MagicMock
from app import Server


def create_server():
    server = MagicMock()
    server.send_response = MagicMock()
    server.send_header = MagicMock()
    server.end_headers = MagicMock()
    server.wfile.write = MagicMock()

    return server


@patch("app.requests.get")
def test_valid_user(mock_get):

    mock_get.return_value.status_code = 200
    mock_get.return_value.content = b'[{"id": "123"}]'

    server = create_server()

    server.path = "/octocat"

    handler = Server.__new__(Server)
    handler.path = "/octocat"
    handler.send_response = server.send_response
    handler.send_header = server.send_header
    handler.end_headers = server.end_headers
    handler.wfile = server.wfile

    handler.do_GET()

    server.send_response.assert_called_with(200)


@patch("app.requests.get")
def test_user_not_found(mock_get):

    mock_get.return_value.status_code = 404
    mock_get.return_value.content = b"User not found"

    handler = Server.__new__(Server)
    handler.path = "/unknown-user"

    handler.send_response = MagicMock()
    handler.end_headers = MagicMock()
    handler.wfile = MagicMock()

    handler.do_GET()

    handler.send_response.assert_called_with(404)


def test_empty_username():

    handler = Server.__new__(Server)
    handler.path = "/"

    handler.send_response = MagicMock()
    handler.end_headers = MagicMock()
    handler.wfile = MagicMock()

    handler.do_GET()

    handler.send_response.assert_called_with(400)


@patch("app.requests.get")
def test_github_rate_limit(mock_get):

    mock_get.return_value.status_code = 403
    mock_get.return_value.content = b"Rate limit exceeded"

    handler = Server.__new__(Server)
    handler.path = "/octocat"

    handler.send_response = MagicMock()
    handler.end_headers = MagicMock()
    handler.wfile = MagicMock()

    handler.do_GET()

    handler.send_response.assert_called_with(403)


@patch("app.requests.get")
def test_github_timeout(mock_get):

    import requests

    mock_get.side_effect = requests.Timeout()

    handler = Server.__new__(Server)
    handler.path = "/octocat"

    handler.send_response = MagicMock()
    handler.end_headers = MagicMock()
    handler.wfile = MagicMock()

    handler.do_GET()

    handler.send_response.assert_called_with(502)