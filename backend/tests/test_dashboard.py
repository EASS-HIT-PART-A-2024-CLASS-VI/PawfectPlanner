import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_dashboard_data():
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)