import pytest
from unittest.mock import patch
from httpx import AsyncClient
from app.main import app

client = AsyncClient(app=app, base_url="http://test")


@pytest.mark.asyncio
async def test_query_gemini_success():
    """Test a successful Gemini query with valid input."""
    with patch("app.routes.gemini.requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "gemini_response": "Your pet is healthy!",
            "weight_message": "Overweight: 40.0kg exceeds the healthy range for Golden Retriever (25.0-35.0kg).",
            "breed_image_url": "http://example.com/golden.jpg"
        }

        payload = {
            "prompt": "Give me health advice",
            "breed": "Golden Retriever",
            "age": "adult",
            "weight": 40.0,
        }
        response = await client.post("/query-gemini", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["gemini_response"] == "Your pet is healthy!"
        assert data["weight_message"].startswith("Overweight")
        assert "breed_image_url" in data


@pytest.mark.asyncio
async def test_query_gemini_invalid_key():
    """Test querying Gemini with an invalid API key."""
    with patch("app.routes.gemini.requests.post") as mock_post:
        mock_post.return_value.status_code = 401
        mock_post.return_value.json.return_value = {"detail": "Invalid API Key"}

        payload = {
            "prompt": "Give me training tips",
            "breed": "Labrador",
            "age": "2 years",
        }

        response = await client.post("/query-gemini", json=payload)

        assert response.status_code == 500  # Should be handled internally as server error
        assert "Error querying Gemini" in response.json()["detail"]


@pytest.mark.asyncio
async def test_query_gemini_invalid_payload():
    """Test querying Gemini with an invalid payload (missing required fields)."""
    response = await client.post("/query-gemini", json={})  # Missing required fields
    assert response.status_code == 422  # Unprocessable Entity
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_query_gemini_no_weight():
    """Test querying Gemini without providing weight."""
    with patch("app.routes.gemini.requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "gemini_response": "Your pet is in great shape!"
        }

        payload = {
            "prompt": "Provide behavior advice",
            "breed": "Bulldog",
            "age": "5 years",
        }
        response = await client.post("/query-gemini", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "gemini_response" in data
        assert "weight_message" not in data  # No weight should be returned


@pytest.mark.asyncio
async def test_query_gemini_puppy_weight():
    """Test Gemini's response for puppies, deferring weight validation to Gemini."""
    with patch("app.routes.gemini.requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "gemini_response": "Puppy weight validation requires Gemini assistance."
        }

        payload = {
            "prompt": "Give me puppy weight advice",
            "breed": "Beagle",
            "age": "puppy",
            "weight": 4.0,
        }
        response = await client.post("/query-gemini", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["gemini_response"] == "Puppy weight validation requires Gemini assistance."


@pytest.mark.asyncio
async def test_query_gemini_health_and_behavior():
    """Test Gemini's response for health and behavior issues."""
    with patch("app.routes.gemini.requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "gemini_response": "Your pet has health and behavior concerns.",
            "breed_image_url": "http://example.com/shepherd.jpg"
        }

        payload = {
            "prompt": "Health and behavior advice",
            "breed": "German Shepherd",
            "age": "5 years",
            "health_issues": ["Hip Dysplasia"],
            "behavior_issues": ["Excessive Barking"],
        }
        response = await client.post("/query-gemini", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "gemini_response" in data
        assert "breed_image_url" in data
