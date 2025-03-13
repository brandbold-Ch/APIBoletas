import pytest


def test_get_academic_histories(client):
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJlbnJvbGxtZW50IjoiMjJBMDcxMDIxN00wMDAxIiwiZXhwIjoxNzQxNzU5MjI1fQ.tlsfUlJg0VLrs0ES6YEWfv67qBSj8_J-yYnbaNhAk0zG6XQmbTsD-THUwUVrRie_bIVLCyp-BNF7Lq0gQCba6w"}

    enrollment = "22A0710217M0001"
    rank = 2
    partial = 1

    response = client.get(
        f"/{enrollment}/histories/?rank={rank}&partial={partial}",
        headers=headers
    )

    assert response.status_code == 200
    assert "HISTORIAL" in response.json()


def test_get_semiannual_academic_histories(client):
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJlbnJvbGxtZW50IjoiMjJBMDcxMDIxN00wMDAxIiwiZXhwIjoxNzQxNzU5MjI1fQ.tlsfUlJg0VLrs0ES6YEWfv67qBSj8_J-yYnbaNhAk0zG6XQmbTsD-THUwUVrRie_bIVLCyp-BNF7Lq0gQCba6w"}

    enrollment = "22A0710217M0001"
    rank = 2

    response = client.get(
        f"/{enrollment}/histories/semiannual/?rank={rank}",
        headers=headers
    )

    assert response.status_code == 200
    assert "DETALLES" in response.json()
