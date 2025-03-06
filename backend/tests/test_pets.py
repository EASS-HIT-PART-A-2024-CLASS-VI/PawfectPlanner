# File: tests/test_pets.py

def _auth_headers(client, email="petuser@example.com", password="petpass"):
    # Helper to quickly get an auth header
    client.post("/auth/register", json={"email": email, "password": password})
    login_res = client.post("/auth/login", json={"email": email, "password": password})
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_pet(client):
    headers = _auth_headers(client)

    # Basic dog creation
    payload = {
        "name": "Fido",
        "type": "dog",
        "breed": "German Shepherd",
        "birth_date": "2019-06-01",
        "weight": 35.0,
        "health_issues": ["allergies"],
        "behavior_issues": ["anxiety"],
        "owner_id": 1
    }
    res = client.post("/pets", json=payload, headers=headers)
    assert res.status_code == 200, res.text
    pet_data = res.json()
    assert pet_data["name"] == "Fido"
    assert pet_data["type"] == "dog"
    assert pet_data["breed"] == "German Shepherd"
    assert "average_weight_range" in pet_data  # fetched from The Dog API if available

def test_list_pets(client):
    headers = _auth_headers(client, email="listpet@example.com")

    # create 2 pets
    client.post("/pets", json={
        "name": "PetA", "type": "dog", "breed": "Bulldog", "owner_id": 1
    }, headers=headers)
    client.post("/pets", json={
        "name": "PetB", "type": "cat", "breed": "Siamese", "owner_id": 1
    }, headers=headers)

    # list them
    res = client.get("/pets", headers=headers)
    assert res.status_code == 200
    pets = res.json()
    assert len(pets) >= 2

def test_get_pet_by_id(client):
    headers = _auth_headers(client, email="singlepet@example.com")

    # create pet
    create_res = client.post("/pets", json={
        "name": "Single",
        "type": "dog",
        "breed": "Golden Retriever",
        "owner_id": 1
    }, headers=headers)
    new_pet = create_res.json()

    # fetch by id
    pet_id = new_pet["id"]
    get_res = client.get(f"/pets/{pet_id}", headers=headers)
    assert get_res.status_code == 200
    got_pet = get_res.json()
    assert got_pet["name"] == "Single"

def test_update_pet(client):
    headers = _auth_headers(client, email="updatepet@example.com")

    # create
    create_res = client.post("/pets", json={
        "name": "UpdateMe",
        "type": "dog",
        "breed": "Beagle",
        "owner_id": 1
    }, headers=headers)
    pet_id = create_res.json()["id"]

    # update
    update_res = client.put(f"/pets/{pet_id}", json={
        "name": "UpdatedName",
        "weight": 12.5
    }, headers=headers)
    assert update_res.status_code == 200
    updated = update_res.json()
    assert updated["name"] == "UpdatedName"
    assert updated["weight"] == 12.5

def test_delete_pet(client):
    headers = _auth_headers(client, email="deletepet@example.com")

    # create
    create_res = client.post("/pets", json={
        "name": "ToDelete",
        "type": "dog",
        "breed": "Labrador",
        "owner_id": 1
    }, headers=headers)
    pet_id = create_res.json()["id"]

    # delete
    del_res = client.delete(f"/pets/{pet_id}", headers=headers)
    assert del_res.status_code == 200
    assert del_res.json()["detail"] == "Pet deleted successfully"

    # confirm it's gone
    get_res = client.get(f"/pets/{pet_id}", headers=headers)
    assert get_res.status_code == 404, get_res.text
