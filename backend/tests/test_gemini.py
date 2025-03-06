# File: tests/test_gemini.py
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

def test_gemini_query_mock(client: TestClient):
    """
    Test the /gemini/query endpoint with a mocked AI response.
    """
    # Suppose your geminiService has a function query_gemini that we can patch
    with patch("backend.gemini_service.geminiRun.client.models.generate_content") as mock_gen:
        # Mock an AI answer
        mock_gen.return_value.text = "Mocked AI response about your pet..."

        # Now do a POST to /gemini/query
        payload = {
            "prompt": "Hello Gemini!",
            "pet": {"name": "MockPet", "weight": 10},
            "forceJSON": False
        }
        res = client.post("/gemini/query", json=payload)
        assert res.status_code == 200, res.text
        data = res.json()
        assert "answer" in data
        assert data["answer"] == "Mocked AI response about your pet..."

        # Ensure the mock was called with the correct arguments
        mock_gen.assert_called_once()
