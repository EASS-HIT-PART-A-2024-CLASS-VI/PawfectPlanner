import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_vaccines():
    """Test fetching all available vaccines for dogs."""
    response = client.get("/api/vaccines?pet_type=dog")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_vaccines_invalid_pet():
    """Test requesting vaccine data for an unsupported pet type."""
    response = client.get("/api/vaccines?pet_type=rabbit")
    assert response.status_code == 400
    assert "Unsupported pet type" in response.json()["detail"]


def test_calculate_vaccine_schedule():
    """Test generating a vaccination schedule."""
    response = client.post("/api/vaccines/schedule", json={
        "birth_date": "2024-01-01",
        "pet_type": "dog"
    })
    assert response.status_code == 200
    assert isinstance(response.json()["schedule"], list)
