from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os

from app.util import validate_weight

app = FastAPI()

# Environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://api.gemini.example/v1/query"
DOG_API_URL = "https://api.thedogapi.com/v1/breeds"
DOG_API_KEY = os.getenv("DOG_API_KEY")


class GeminiPrompt(BaseModel):
    prompt: str
    breed: str
    age: Optional[str] = None
    weight: Optional[float] = None


@app.post("/query-gemini")
async def query_gemini(data: GeminiPrompt):
    """
    Handles Gemini queries and integrates breed facts and images.
    """
    if not data.prompt:
        raise HTTPException(status_code=400, detail="Prompt is required.")

    # Attach weight validation for adult pets
    weight_message = None
    if data.weight and data.age != "puppy":
        weight_message = validate_weight(data.breed, data.weight)

    try:
        # Build prompt for Gemini API
        prompt = data.prompt
        if data.breed:
            prompt += f" Breed: {data.breed}."
        if data.age:
            prompt += f" Age: {data.age}."
        if data.weight:
            prompt += f" Weight: {data.weight} kg."

        payload = {"prompt": prompt}
        headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}

        # Query Gemini API
        async with httpx.AsyncClient() as client:
            response = await client.post(GEMINI_URL, json=payload, headers=headers)
            response.raise_for_status()

        # Fetch breed image
        breed_image_url = await fetch_breed_image(data.breed) if data.breed else None

        # Combine responses
        gemini_response = response.json()
        return {
            "gemini_response": gemini_response,
            "weight_message": weight_message,
            "breed_image_url": breed_image_url,
        }

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error querying Gemini: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=response.status_code, detail=response.text)


async def fetch_breed_image(breed: str) -> Optional[str]:
    """
    Fetches an image URL for the given breed from The Dog API.
    """
    try:
        headers = {"x-api-key": DOG_API_KEY}
        async with httpx.AsyncClient() as client:
            response = await client.get(DOG_API_URL, headers=headers)
            response.raise_for_status()

        breeds = response.json()
        for b in breeds:
            if b["name"].lower() == breed.lower():
                return b.get("image", {}).get("url")

        return None  # Breed not found
    except httpx.RequestError:
        return None  # Handle API error gracefully
