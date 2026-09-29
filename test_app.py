import requests


def test_valid_user():

    response = requests.get(
        "http://localhost:8080/octocat"
    )

    assert response.status_code == 200


def test_user_not_found():

    response = requests.get(
        "http://localhost:8080/this-user-does-not-exist-123456"
    )

    assert response.status_code == 404


def test_empty_username():

    response = requests.get(
        "http://localhost:8080/"
    )

    assert response.status_code == 400