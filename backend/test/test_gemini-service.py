import pytest
from httpx import AsyncClient
from backend.gemini_service import app


@pytest.mark.asyncio
async def test_query_gemini_success():
    """
    Test a successful Gemini query with valid input.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "prompt": "Give me health advice",
            "breed": "Golden Retriever",
            "age": "adult",
            "weight": 40.0,
        }
        response = await client.post("/query-gemini", json=payload)

        assert response.status_code == 200
        data = response.json()

        # Assertions for response structure and expected values
        assert "gemini_response" in data
        assert "weight_message" in data
        assert data["weight_message"] == "Overweight: 40.0kg exceeds the healthy range for Golden Retriever (25.0-35.0kg)."
        assert "breed_image_url" in data


@pytest.mark.asyncio
async def test_query_gemini_invalid_key():
    """
    Test querying Gemini with an invalid API key.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "prompt": "Give me training tips",
            "breed": "Labrador",
            "age": "2 years",
        }
        # Temporarily replace the environment variable to simulate invalid key
        original_key = app.GEMINI_API_KEY
        app.GEMINI_API_KEY = "INVALID_KEY"

        response = await client.post("/query-gemini", json=payload)

        assert response.status_code == 500
        assert "Error querying Gemini" in response.json()["detail"]

        # Restore the original API key
        app.GEMINI_API_KEY = original_key


@pytest.mark.asyncio
async def test_query_gemini_invalid_payload():
    """
    Test querying Gemini with an invalid payload (missing required fields).
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {}  # Missing required fields like 'prompt', 'breed', and 'age'
        response = await client.post("/query-gemini", json=payload)

        assert response.status_code == 422  # Unprocessable Entity
        assert "detail" in response.json()


@pytest.mark.asyncio
async def test_query_gemini_no_weight():
    """
    Test querying Gemini without providing weight.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "prompt": "Provide behavior advice",
            "breed": "Bulldog",
            "age": "5 years",
        }
        response = await client.post("/query-gemini", json=payload)

        assert response.status_code == 200
        data = response.json()

        assert "gemini_response" in data
        assert "weight_message" not in data  # Weight message should not exist


@pytest.mark.asyncio
async def test_query_gemini_puppy_weight():
    """
    Test Gemini's response for puppies, deferring weight validation to Gemini.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "prompt": "Give me puppy weight advice",
            "breed": "Beagle",
            "age": "puppy",
            "weight": 4.0,
        }
        response = await client.post("/query-gemini", json=payload)

        assert response.status_code == 200
        data = response.json()

        assert "gemini_response" in data
        assert data["gemini_response"] == "Puppy weight validation requires Gemini assistance."


@pytest.mark.asyncio
async def test_query_gemini_health_and_behavior():
    """
    Test Gemini's response for health and behavior issues.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
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
        assert "weight_message" not in data  # No weight provided
        assert "breed_image_url" in data
