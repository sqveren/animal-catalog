from app.database import Base, get_db


def test_create_adoption(client):
    create_animal_response = client.post("/animals", json={
        "name": "Bella",
        "species": "cat",
        "breed": "Siamese",
        "age": 2,
        "arrival_date": "2026-09-05",
        "description": "Calm cat"
    })

    animal_id = create_animal_response.json()["id"]

    create_adopter_response = client.post("/adopters", json={
        "first_name": "Anatolii",
        "last_name": "Doe",
        "email": "ijijed@gmail.com",
        "phone_number": "+38056743657",
    })

    adopter_id = create_adopter_response.json()["id"]


    create_adoption_response = client.post("/adoptions", json={
        "animal_id": animal_id,
        "adopter_id": adopter_id
    })


    assert create_adoption_response.status_code == 201
    assert create_adoption_response.json()["status"] == "pending"

    animal_check = client.get(f"/animals/{animal_id}")
    assert animal_check.json()["status"] == "pending"

def test_adoption_not_available(client):
    create_animal_response = client.post("/animals", json={
        "name": "Bella",
        "species": "cat",
        "breed": "Siamese",
        "age": 2,
        "arrival_date": "2026-09-05",
        "description": "Calm cat"
    })

    animal_id = create_animal_response.json()["id"]

    create_adopter_response = client.post("/adopters", json={
        "first_name": "Anatolii",
        "last_name": "Doe",
        "email": "ijijed@gmail.com",
        "phone_number": "+38056743657",
    })

    adopter_id = create_adopter_response.json()["id"]


    create_adoption_response = client.post("/adoptions", json={
        "animal_id": animal_id,
        "adopter_id": adopter_id
    })

    create_second_response = client.post("/adoptions", json={
        "animal_id": animal_id,
        "adopter_id": adopter_id
    })
    assert create_second_response.status_code == 400

def test_create_adoption_animal_not_found(client):
    adopter_response = client.post("/adopters", json={
        "first_name": "Petro", "last_name": "Sydorenko",
        "email": "petro@example.com", "phone_number": None
    })
    adopter_id = adopter_response.json()["id"]

    response = client.post("/adoptions", json={
        "animal_id": 999999,
        "adopter_id": adopter_id
    })
    assert response.status_code == 404