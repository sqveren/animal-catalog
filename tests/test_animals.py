def test_create_animal(client, auth_headers):
    response = client.post("/animals", json={
        "name": "Rex",
        "species": "dog",
        "breed": "Labrador",
        "age": 3,
        "arrival_date": "2026-09-01",
        "description": "Friendly dog"
    }, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Rex"
    assert "id" in data
    assert data["status"] == "available"


def test_get_animal_not_found(client):
    response = client.get("/animals/99999")
    assert response.status_code == 404


def test_get_animal_success(client, auth_headers):
    create_response = client.post("/animals", json={
        "name": "Bella",
        "species": "cat",
        "breed": "Siamese",
        "age": 2,
        "arrival_date": "2026-09-05",
        "description": "Calm cat"
    }, headers=auth_headers)
    animal_id = create_response.json()["id"]

    response = client.get(f"/animals/{animal_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Bella"


def test_delete_animal(client, auth_headers):
    create_response = client.post("/animals", json={
        "name": "Max", "species": "dog", "breed": "Poodle",
        "age": 4, "arrival_date": "2026-09-01", "description": ""
    }, headers=auth_headers)
    animal_id = create_response.json()["id"]

    delete_response = client.delete(f"/animals/{animal_id}", headers=auth_headers)
    assert delete_response.status_code == 204

    get_response = client.get(f"/animals/{animal_id}")
    assert get_response.status_code == 404