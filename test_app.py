import json
from unittest.mock import patch
from http.client import HTTPConnection

from app import Server
from http.server import HTTPServer
import threading


def start_server():
    server = HTTPServer(("localhost", 8090), Server)

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True
    )

    thread.start()

    return server


@patch("app.requests.get")
def test_valid_user(mock_get):

    mock_get.return_value.status_code = 200
    mock_get.return_value.content = b'[{"id": "123"}]'

    server = start_server()

    connection = HTTPConnection("localhost", 8090)
    connection.request("GET", "/octocat")

    response = connection.getresponse()

    assert response.status == 200
    assert json.loads(response.read()) == [{"id": "123"}]

    server.shutdown()


@patch("app.requests.get")
def test_user_not_found(mock_get):

    mock_get.return_value.status_code = 404
    mock_get.return_value.content = b"User not found"

    server = start_server()

    connection = HTTPConnection("localhost", 8090)
    connection.request("GET", "/unknown-user")

    response = connection.getresponse()

    assert response.status == 404

    server.shutdown()


def test_empty_username():

    server = start_server()

    connection = HTTPConnection("localhost", 8090)
    connection.request("GET", "/")

    response = connection.getresponse()

    assert response.status == 400

    server.shutdown()


@patch("app.requests.get")
def test_github_rate_limit(mock_get):

    mock_get.return_value.status_code = 403
    mock_get.return_value.content = b"Rate limit exceeded"

    server = start_server()

    connection = HTTPConnection("localhost", 8090)
    connection.request("GET", "/octocat")

    response = connection.getresponse()

    assert response.status == 403

    server.shutdown()


@patch("app.requests.get")
def test_github_timeout(mock_get):

    import requests

    mock_get.side_effect = requests.Timeout()

    server = start_server()

    connection = HTTPConnection("localhost", 8090)
    connection.request("GET", "/octocat")

    response = connection.getresponse()

    assert response.status == 502

    server.shutdown()