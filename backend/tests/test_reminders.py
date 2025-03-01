import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_reminder():
    response = client.post("/api/reminders", json={"title": "Vet Visit", "date": "2025-01-30", "pet_id": 1})
    assert response.status_code == 200

def test_fetch_reminders():
    response = client.get("/api/reminders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)