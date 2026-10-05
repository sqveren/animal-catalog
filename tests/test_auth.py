def test_create_animal_without_token(client):
    response = client.post("/animals", json={
        "name": "Rex", "species": "dog", "breed": "Labrador",
        "age": 3, "arrival_date": "2026-09-01", "description": ""
    })
    assert response.status_code == 401


def test_login_wrong_password(client):
    client.post("/auth/register", json={"username": "admin", "password": "secret123"})
    response = client.post("/auth/login", data={"username": "admin", "password": "wrong"})
    assert response.status_code == 401


def test_register_duplicate_username(client, auth_headers):
    client.post("/auth/register", json={"username": "admin2", "password": "secret123"}, headers=auth_headers)
    response = client.post("/auth/register", json={"username": "admin", "password": "other"}, headers=auth_headers)
    assert response.status_code == 400

def test_register_without_token(client):
    response = client.post("/auth/register", json={"username": "newuser", "password": "pass123"})
    assert response.status_code == 401