from app.database import Base, get_db



def test_create_adopter(client):
    response = client.post("/adopters", json ={
        "first_name": "Anatolii",
        "last_name": "Doe",
        "email": "ijijed@gmail.com",
        "phone_number": "+38056743657",
    })

    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "Anatolii"
    assert "id" in data


def test_get_adopter_success(client):
    response_client = client.post("/adopters", json ={
        "first_name": "Anatolii",
        "last_name": "Doe",
        "email": "ijijed@gmail.com",
        "phone_number": "+38056743657",
    })

    adopter_id = response_client.json()["id"]

    response = client.get(f"/adopters/{adopter_id}")
    assert response.status_code == 200
    assert response.json()["first_name"] == "Anatolii"


def test_get_invalid_adopter(client):
    response = client.get(f"/adopters/999999")
    assert response.status_code == 404


def test_delete_adopter(client):
    response_client = client.post("/adopters", json ={
        "first_name": "Anatolii",
        "last_name": "Doe",
        "email": "ijijed@gmail.com",
        "phone_number": "+38056743657",
    })

    adopter_id = response_client.json()["id"]

    response_delete = client.delete(f"/adopters/{adopter_id}")
    assert response_delete.status_code == 204

    response_get = client.get(f"/adopters/{adopter_id}")
    assert response_get.status_code == 404





