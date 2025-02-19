import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_vaccines_dog():
    """
    Test fetching vaccination data for dogs.
    """
    response = client.get("/api/vaccines?pet_type=dog")
    assert response.status_code == 200
    data = response.json()
    assert "mandatory" in data
    assert "recommended" in data

def test_get_vaccines_cat():
    """
    Test fetching vaccination data for cats.
    """
    response = client.get("/api/vaccines?pet_type=cat")
    assert response.status_code == 200
    data = response.json()
    assert "mandatory" in data
    assert "recommended" in data

def test_get_vaccines_invalid_pet_type():
    """
    Test fetching vaccination data with an invalid pet type.
    """
    response = client.get("/api/vaccines?pet_type=bird")
    assert response.status_code == 404
    assert response.json() == {"detail": "Vaccination data not found."}

def test_calculate_vaccine_schedule_dog():
    """
    Test calculating a vaccination schedule for a dog.
    """
    response = client.post("/api/vaccines/schedule", json={"birth_date": "2023-01-01", "pet_type": "dog"})
    assert response.status_code == 200
    data = response.json()
    assert "schedule" in data
    assert isinstance(data["schedule"], list)

def test_calculate_vaccine_schedule_cat():
    """
    Test calculating a vaccination schedule for a cat.
    """
    response = client.post("/api/vaccines/schedule", json={"birth_date": "2023-01-01", "pet_type": "cat"})
    assert response.status_code == 200
    data = response.json()
    assert "schedule" in data
    assert isinstance(data["schedule"], list)

def test_calculate_vaccine_schedule_invalid_date():
    """
    Test calculating a vaccination schedule with an invalid date.
    """
    response = client.post("/api/vaccines/schedule", json={"birth_date": "invalid-date", "pet_type": "dog"})
    assert response.status_code == 500
    assert "detail" in response.json()

def test_calculate_vaccine_schedule_missing_pet_type():
    """
    Test calculating a vaccination schedule with a missing pet type.
    """
    response = client.post("/api/vaccines/schedule", json={"birth_date": "2023-01-01"})
    assert response.status_code == 422  # Unprocessable Entity
