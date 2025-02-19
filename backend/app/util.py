import os
import requests
from dotenv import load_dotenv
from functools import lru_cache
from typing import Optional
from fastapi import HTTPException


# Load environment variables from .env
load_dotenv()

# API details
DOG_API_URL = "https://api.thedogapi.com/v1"
API_KEY = os.getenv("DOG_API_KEY")

def make_api_call(endpoint: str, params: dict = None) -> dict:
    """
    Generic function to make API calls to The Dog API.
    Args:
        endpoint (str): The API endpoint (e.g., '/breeds').
        params (dict): Query parameters for the API call.
    Returns:
        dict: The JSON response from the API, or an error message.
    """
    headers = {"x-api-key": API_KEY}  # API key in headers
    try:
        response = requests.get(f"{DOG_API_URL}{endpoint}", headers=headers, params=params)
        response.raise_for_status()  # Raise HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except requests.exceptions.RequestException as req_err:
        return {"error": f"Request error occurred: {req_err}"}

@lru_cache(maxsize=100)
def fetch_all_breeds():
    """
    Fetch all breeds from the API and cache the result.
    Returns:
        list: A list of all breeds, or an empty list if the API call fails.
    """
    headers = {"x-api-key": API_KEY}
    try:
        response = requests.get(f"{DOG_API_URL}/breeds", headers=headers)
        response.raise_for_status()
        return response.json()  # Cache this result
    except requests.exceptions.RequestException as e:
        print(f"Error fetching breeds: {e}")
        return []

def validate_weight(breed: str, weight: float, age: Optional[int] = None, is_puppy: bool = False) -> str:
    """
    Validates the pet's weight based on its breed and age.
    If the pet is a puppy, additional logic applies via Gemini.
    """
    # Dummy weight ranges for demonstration; replace with Dog API data.
    weight_ranges = {
        "Golden Retriever": (55, 75),
        "Labrador": (55, 80),
        # Add other breeds here
    }

    if breed not in weight_ranges and not is_puppy:
        raise HTTPException(status_code=404, detail="Breed weight range not available.")

    if is_puppy:
        # Query Gemini for puppy-specific ranges
        response = requests.post(
            "http://gemini-service:8000/query",
            json={"prompt": f"What is the healthy weight range for a {age}-month-old {breed} puppy?"},
        )
        data = response.json()
        if "weight_range" in data:
            min_weight, max_weight = map(float, data["weight_range"].split("-"))
        else:
            raise HTTPException(status_code=500, detail="Error fetching weight range for puppies.")
    else:
        min_weight, max_weight = weight_ranges[breed]

    if weight < min_weight:
        return "underweight"
    elif weight > max_weight:
        return "overweight"
    return "healthy"

def validate_weight(breed: str, weight: float, is_puppy: bool = False) -> Optional[str]:
    """
    Validates the pet's weight against breed standards.
    For puppies, defers to Gemini for advice.
    Returns a notification message if the weight is out of range, otherwise None.
    """
    # Example breed weight ranges (data should come from The Dog API or The Cat API)
    breed_weight_ranges = {
        "Golden Retriever": (25.0, 35.0),  # in kilograms
        "Siamese": (4.0, 6.0),
        "other": None,  # No weight range for "other"
    }

    if is_puppy:
        return "Puppy weight validation requires Gemini assistance."

    # Check if the breed is supported
    if breed not in breed_weight_ranges or not breed_weight_ranges[breed]:
        return None  # Skip validation for unsupported breeds

    min_weight, max_weight = breed_weight_ranges[breed]
    if weight < min_weight:
        return f"Underweight: {weight}kg is below the healthy range for {breed} ({min_weight}-{max_weight}kg)."
    elif weight > max_weight:
        return f"Overweight: {weight}kg exceeds the healthy range for {breed} ({min_weight}-{max_weight}kg)."

    return None  # Weight is within the healthy range
