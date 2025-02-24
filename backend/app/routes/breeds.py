import os
import redis
import json
import httpx
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

router = APIRouter()

DOG_API_KEY = os.getenv("DOG_API_KEY")
CACHE_EXPIRATION = 3600  # Cache expires in 1 hour

# Initialize Redis cache
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


@router.get("/breeds/{pet_type}/{breed_name}")
def get_breed_info(pet_type: str, breed_name: str):
    """
    Fetch breed information for dogs or cats.
    If breed_name is "other", return a generic response.
    Caching is implemented to reduce API calls.
    """
    breed_name = breed_name.lower()

    # Handle "other" breed case
    if breed_name == "other":
        return {
            "info": "No breed-specific information available. However, you can still access vaccination schedules, custom treatments, reminders, and AI features."
        }

    # Check cache before making an API call
    cache_key = f"{pet_type}_breed_{breed_name}"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)

    # Define API endpoints
    if pet_type.lower() == "dog":
        url = f"https://api.thedogapi.com/v1/breeds/search?q={breed_name}"
        headers = {"x-api-key": DOG_API_KEY} if DOG_API_KEY else {}
    elif pet_type.lower() == "cat":
        url = f"https://api.thecatapi.com/v1/breeds/search?q={breed_name}"
        headers = {}  # The Cat API does not require an API key for breed searches
    else:
        raise HTTPException(status_code=400, detail="Invalid pet type. Use 'dog' or 'cat'.")

    # Make API request
    try:
        response = httpx.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data:
            breed_info = data[0]  # Return first breed match
            redis_client.setex(cache_key, CACHE_EXPIRATION, json.dumps(breed_info))  # Cache the response
            return breed_info
        else:
            raise HTTPException(status_code=404, detail="Breed not found.")

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"API error: {e.response.text}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching breed data: {str(e)}")
