import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_other_breed_info():
    # Test for "Other" breed
    response = client.get("/breeds/dog/other")
    assert response.status_code == 200
    assert response.json() == {
        "info": "No breed-specific information available. However, you can still access vaccination schedules and reminders."
    }

def test_invalid_pet_type():
    # Test for invalid pet type
    response = client.get("/breeds/invalid/Golden Retriever")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid pet type. Use 'dog' or 'cat'."
