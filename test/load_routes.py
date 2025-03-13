import pytest


def test_get_academic_load(client):
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJlbnJvbGxtZW50IjoiMjJBMDcxMDIxN00wMDAxIiwiZXhwIjoxNzQxNzU5MjI1fQ.tlsfUlJg0VLrs0ES6YEWfv67qBSj8_J-yYnbaNhAk0zG6XQmbTsD-THUwUVrRie_bIVLCyp-BNF7Lq0gQCba6w"}

    enrollment = "22A0710217M0001"
    partial = 1

    response = client.get(
        f"/{enrollment}/loads/?partial={partial}",
        headers=headers
    )

    assert response.status_code == 200
    assert "CARGA" in response.json()


def test_get_semiannual_academic_load(client):
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJlbnJvbGxtZW50IjoiMjJBMDcxMDIxN00wMDAxIiwiZXhwIjoxNzQxNzU5MjI1fQ.tlsfUlJg0VLrs0ES6YEWfv67qBSj8_J-yYnbaNhAk0zG6XQmbTsD-THUwUVrRie_bIVLCyp-BNF7Lq0gQCba6w"}

    enrollment = "22A0710217M0001"

    response = client.get(
        f"/{enrollment}/loads/semiannual",
        headers=headers
    )

    assert response.status_code == 200
    assert "semiannual_load" in response.json()
