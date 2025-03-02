import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_create_pet():
    """Test creating a new pet."""
    pet_data = {
        "name": "Buddy",
        "type": "dog",
        "breed": "golden_retriever",
        "weight": 25
    }
    response = client.post("/api/pets/", json=pet_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Buddy"


def test_get_pets():
    """Test retrieving the list of pets."""
    response = client.get("/api/pets/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_pet_by_id():
    """Test retrieving a single pet by ID."""
    response = client.get("/api/pets/1")
    assert response.status_code == 200
    assert "name" in response.json()


def test_update_pet():
    """Test updating pet details."""
    update_data = {"name": "BuddyUpdated", "weight": 28}
    response = client.put("/api/pets/1", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == "BuddyUpdated"


def test_delete_pet():
    """Test deleting a pet."""
    response = client.delete("/api/pets/1")
    assert response.status_code == 200
