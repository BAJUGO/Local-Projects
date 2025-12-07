from fastapi.testclient import TestClient
from unittest.mock import patch




def test_hello(client):
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world"}


def test_hello_someone(client):
    response = client.get("/hello?name=Alice")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Alice"}


def test_hello_int(client):
    response = client.get("/hello?name=4")
    assert response.status_code == 400
    assert response.json() == {"detail": "You can't do int"}


def test_joke(client):
    fake_response = {"value": "Chuck Norris can test your code automatically."}
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = fake_response

        response = client.get("/jokes")
        assert response.status_code == 200
        assert response.json() == {"joke": fake_response["value"]}