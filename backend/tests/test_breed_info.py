# File: tests/test_breed_info.py
from unittest.mock import patch
from fastapi.testclient import TestClient

def test_fetch_dog_breed_info(client: TestClient):
    with patch("backend.routes.pets.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{
            "weight": {"metric": "25 - 34"},
            "life_span": "10 - 12 years",
            "temperament": "Friendly, Loyal"
        }]
        # Now create a pet that triggers fetch_breed_info
        payload = {
            "name": "TestDog",
            "type": "dog",
            "breed": "Golden Retriever",
            "owner_id": 1
        }
        # You also need auth headers if your endpoint requires auth
        client.post("/auth/register", json={"email":"test@dog.com","password":"p"})
        token = client.post("/auth/login", json={"email":"test@dog.com","password":"p"}).json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        res = client.post("/pets", json=payload, headers=headers)
        assert res.status_code == 200
        data = res.json()
        assert data["average_weight_range"] == "25 - 34"
        assert data["life_expectancy"] == "10 - 12 years"
        assert data["temperament"] == "Friendly, Loyal"

        # Check that mock_get was called with the correct The Dog API endpoint
        assert mock_get.call_args[0][0].startswith("https://api.thedogapi.com/v1/breeds/search?q=golden retriever")
