import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestBreeds:
    """
    Tests for Dog and Cat breed API integrations.
    """

    def test_fetch_dog_breeds(self):
        """
        Test if the application can fetch data from The Dog API.
        """
        response = client.get("/api/breeds/dogs")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0  # Ensure some breeds are returned
        assert "name" in data[0]  # Verify the structure

    def test_fetch_cat_breeds(self):
        """
        Test if the application can fetch data from The Cat API.
        """
        response = client.get("/api/breeds/cats")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0  # Ensure some breeds are returned
        assert "name" in data[0]  # Verify the structure

    @patch("app.routes.breeds.requests.get")
    def test_fetch_dog_breeds_mocked(self, mock_get):
        """
        Test Dog API integration with mocked response.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"name": "Golden Retriever", "id": 1},
            {"name": "Labrador Retriever", "id": 2},
        ]

        response = client.get("/api/breeds/dogs")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "Golden Retriever"

    @patch("app.routes.breeds.requests.get")
    def test_fetch_cat_breeds_mocked(self, mock_get):
        """
        Test Cat API integration with mocked response.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"name": "Persian Cat", "id": 101},
            {"name": "Siamese Cat", "id": 102},
        ]

        response = client.get("/api/breeds/cats")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "Persian Cat"
