import requests

def test_octocat():

    response = requests.get(
        "http://localhost:8080/octocat",
        timeout=10
    )

    assert response.status_code == 200