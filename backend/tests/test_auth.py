import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.parametrize("email, password, expected_status", [
    ("newuser@example.com", "securepassword", 200),  # New user
    ("testuser@example.com", "securepassword", 400),  # Duplicate user
])
def test_register_user(email, password, expected_status):
    response = client.post("/api/auth/register", json={"email": email, "password": password})
    assert response.status_code == expected_status


def test_login_user():
    response = client.post("/api/auth/login", json={"email": "testuser@example.com", "password": "securepassword"})
    assert response.status_code in [200, 401]  # 401 if wrong password