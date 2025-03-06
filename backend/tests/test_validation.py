# File: tests/test_validation.py

def _auth_headers(client):
    client.post("/auth/register", json={"email": "valid@example.com", "password": "validpass"})
    token = client.post("/auth/login", json={"email": "valid@example.com", "password": "validpass"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_pet_negative_weight(client):
    headers = _auth_headers(client)
    payload = {
        "name": "NegativeWeight",
        "type": "dog",
        "breed": "Bulldog",
        "weight": -5,
        "owner_id": 1
    }
    res = client.post("/pets", json=payload, headers=headers)
    assert res.status_code == 422, res.text
    # Optionally parse the error detail

def test_pet_future_birthdate(client):
    headers = _auth_headers(client)
    payload = {
        "name": "TimeTraveler",
        "type": "cat",
        "breed": "Siamese",
        "birth_date": "3025-01-01",
        "owner_id": 1
    }
    res = client.post("/pets", json=payload, headers=headers)
    assert res.status_code == 422, res.text

def test_pet_exceed_weight_for_dog(client):
    headers = _auth_headers(client)
    payload = {
        "name": "ElephantDog",
        "type": "dog",
        "breed": "Labrador",
        "weight": 300,  # over 200 for dog
        "owner_id": 1
    }
    res = client.post("/pets", json=payload, headers=headers)
    assert res.status_code == 422, res.text
