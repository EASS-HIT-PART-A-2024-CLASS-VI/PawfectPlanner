import httpx
import os

GEMINI_SERVICE_URL = "http://gemini-service:11434/gemini"

def query_gemini(prompt: str):
    try:
        response = httpx.post(GEMINI_SERVICE_URL, json={"prompt": prompt})
        response.raise_for_status()
        print("Response from Gemini:", response.json())
    except httpx.RequestError as e:
        print(f"Request error: {e}")
    except httpx.HTTPStatusError as e:
        print(f"HTTP error {e.response.status_code}: {e.response.text}")

if __name__ == "__main__":
    query_gemini("Tell me a random fact about Golden Retrievers.")
