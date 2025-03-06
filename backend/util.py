# File: backend/util.py

import os
import logging
import requests
from dotenv import load_dotenv
from functools import lru_cache
from fastapi import HTTPException

# ✅ Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Load .env file correctly
load_dotenv()

# API Configuration
DOG_API_URL = "https://api.thedogapi.com/v1"
DOG_API_KEY = os.getenv("DOG_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

if not DOG_API_KEY:
    logger.warning("⚠️ DOG_API_KEY is missing! Set it in .env file.")

if not GEMINI_API_KEY:
    logger.warning("⚠️ GEMINI_API_KEY is missing! Some features may not work.")

def make_api_call(endpoint: str, params: dict = None) -> dict:
    """
    Generic function to make API calls to The Dog API.
    """
    headers = {"x-api-key": DOG_API_KEY} if DOG_API_KEY else {}
    try:
        response = requests.get(f"{DOG_API_URL}{endpoint}", headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as req_err:
        logger.error(f"❌ API Request Error: {req_err}")
        raise HTTPException(status_code=500, detail=f"API Request Error: {str(req_err)}")

@lru_cache(maxsize=100)
def fetch_all_breeds():
    """
    Fetch all breeds from the API and cache the result.
    """
    try:
        return make_api_call("/breeds")
    except HTTPException as e:
        logger.error(f"❌ Failed to fetch breeds: {e.detail}")
        return []

def validate_weight(breed: str, weight: float, is_puppy: bool = False):
    """
    Validates the pet's weight against known breed ranges.
    """
    breed_weight_ranges = {
        "Golden Retriever": (25.0, 35.0),  # in kg
        "Siamese": (4.0, 6.0),
    }

    if is_puppy:
        return "Puppy weight validation requires Gemini assistance."

    if breed not in breed_weight_ranges:
        return None

    min_w, max_w = breed_weight_ranges[breed]
    if weight < min_w:
        return f"⚠️ Underweight: {weight}kg is below the healthy range for {breed} ({min_w}-{max_w}kg)."
    if weight > max_w:
        return f"⚠️ Overweight: {weight}kg exceeds the healthy range for {breed} ({min_w}-{max_w}kg)."

    return None  # Weight is within range
