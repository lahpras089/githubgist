import requests
import threading
from unittest.mock import patch
from http.server import HTTPServer

from app import Server


def start_server():
    # 0 = automatically choose a free port
    server = HTTPServer(("localhost", 0), Server)

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True
    )

    thread.start()

    return server


def make_request(server, path):
    # Get the port selected by the operating system
    port = server.server_address[1]

    response = requests.get(
        f"http://localhost:{port}{path}",
        timeout=10
    )

    return response


@patch("app.requests.get")
def test_valid_user(mock_get):

    mock_get.return_value.status_code = 200
    mock_get.return_value.content = b'[{"id": "123"}]'

    server = start_server()

    response = make_request(server, "/octocat")

    assert response.status_code == 200
    assert response.json() == [{"id": "123"}]

    server.shutdown()
    server.server_close()


@patch("app.requests.get")
def test_user_not_found(mock_get):

    mock_get.return_value.status_code = 404
    mock_get.return_value.content = b"User not found"

    server = start_server()

    response = make_request(server, "/unknown-user")

    assert response.status_code == 404

    server.shutdown()
    server.server_close()


def test_empty_username():

    server = start_server()

    response = make_request(server, "/")

    assert response.status_code == 400

    server.shutdown()
    server.server_close()


@patch("app.requests.get")
def test_github_rate_limit(mock_get):

    mock_get.return_value.status_code = 403
    mock_get.return_value.content = b"Rate limit exceeded"

    server = start_server()

    response = make_request(server, "/octocat")

    assert response.status_code == 403

    server.shutdown()
    server.server_close()


@patch("app.requests.get")
def test_github_timeout(mock_get):

    mock_get.side_effect = requests.Timeout()

    server = start_server()

    response = make_request(server, "/octocat")

    assert response.status_code == 502

    server.shutdown()
    server.server_close()