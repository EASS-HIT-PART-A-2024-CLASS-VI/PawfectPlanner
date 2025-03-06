# File: backend/routes/breeds.py

import os
import httpx
from fastapi import APIRouter, HTTPException

router = APIRouter()

DOG_API_KEY = os.getenv("DOG_API_KEY")

@router.get("/{pet_type}/{breed_name}")
def get_breed_info(pet_type: str, breed_name: str):
    """Fetch breed information for dogs or cats (no caching)."""
    breed_name = breed_name.lower()

    # If breed_name == 'other', just respond with no data
    if breed_name == "other":
        return {"info": "No breed-specific data available."}

    # Decide which API to call
    if pet_type.lower() == "dog":
        url = f"https://api.thedogapi.com/v1/breeds/search?q={breed_name}"
        headers = {"x-api-key": DOG_API_KEY} if DOG_API_KEY else {}
    elif pet_type.lower() == "cat":
        url = f"https://api.thecatapi.com/v1/breeds/search?q={breed_name}"
        headers = {}
    else:
        raise HTTPException(status_code=400, detail="Invalid pet type. Use 'dog' or 'cat'.")

    try:
        response = httpx.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data:
            return data
        else:
            raise HTTPException(status_code=404, detail="Breed not found.")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching breed data: {str(e)}")
