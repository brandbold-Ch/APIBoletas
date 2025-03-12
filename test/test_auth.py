import pytest


def test_login_success(client):
    login_data = {
        "username": "CAFA070122HCSBLNA2",
        "password": "22A0710217M0001"
    }

    response = client.post("/auth/login", json=login_data)

    assert response.status_code == 200
    assert "token" in response.json()


def test_login_failure(client):
    login_data = {
        "username": "CAFA070122HCSBLNA2",
        "password": "22A0710217M0002"
    }

    response = client.post("/auth/login", json=login_data)

    assert response.status_code in [400, 401, 404]
    assert "detail" in response.json() or "details" in response.json()
