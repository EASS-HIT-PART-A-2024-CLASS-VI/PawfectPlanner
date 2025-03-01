import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_treatment():
    """Test adding a treatment for a pet."""
    treatment_data = {
        "pet_id": 1,
        "name": "Rabies Vaccine",
        "date_administered": "2025-02-01",
        "next_due_date": "2026-02-01"
    }
    response = client.post("/api/treatments/pets/1/treatments", json=treatment_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Rabies Vaccine"


def test_get_treatments():
    """Test retrieving all treatments for a pet."""
    response = client.get("/api/treatments/pets/1/treatments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_treatment():
    """Test updating an existing treatment."""
    update_data = {"name": "Updated Treatment", "next_due_date": "2027-02-01"}
    response = client.put("/api/treatments/pets/1/treatments/1", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Treatment"


def test_delete_treatment():
    """Test deleting a treatment."""
    response = client.delete("/api/treatments/pets/1/treatments/1")
    assert response.status_code == 200
