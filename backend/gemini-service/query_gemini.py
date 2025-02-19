import httpx
from fastapi import APIRouter, HTTPException
from app.schemas import Pet
import os

router = APIRouter()

GEMINI_API_URL = "https://gemini-api.example.com/v1/generate"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


@router.post("/gemini/facts")
def generate_pet_facts(pet: Pet):
    """
    Generates facts or advice about a pet using GEMINI.
    """
    if pet.breed == "other" and not pet.other_breed:
        raise HTTPException(status_code=400, detail="other_breed is required when breed is 'other'.")

    # Check for irregular inputs
    errors = []
    if pet.weight and (pet.weight <= 0 or pet.weight > 200):  # Unlikely weight range
        errors.append(f"Weight ({pet.weight} kg) is not typical for a {pet.type}.")
    if pet.birth_date and pet.birth_date.year < 2000:  # Implausible birth year
        errors.append(f"Birth date ({pet.birth_date}) seems irregular.")

    if errors:
        # Call GEMINI to generate a more human-readable error explanation
        prompt = f"Elaborate on the following input issues for a {pet.type}: {', '.join(errors)}"
        response = _call_gemini(prompt)
        return {"errors": errors, "elaboration": response.get("response")}

    # Build GEMINI prompt
    breed_info = pet.other_breed if pet.breed == "other" else pet.breed
    prompt = (
        f"Provide some facts and advice about a {breed_info} "
        f"that is a {pet.type}. "
    )
    if pet.birth_date:
        prompt += f"The pet was born on {pet.birth_date}. "
    if pet.weight:
        prompt += f"The pet weighs approximately {pet.weight} kg."

    response = _call_gemini(prompt)
    return response


@router.post("/gemini/training")
def generate_training_advice(pet: Pet):
    """
    Provides training advice for a pet based on its breed, age, and known behavior issues.
    """
    if pet.breed == "other" and not pet.other_breed:
        raise HTTPException(status_code=400, detail="other_breed is required when breed is 'other'.")

    breed_info = pet.other_breed if pet.breed == "other" else pet.breed
    prompt = f"Give training advice for a {breed_info} {pet.type}. "
    if pet.birth_date:
        prompt += f"The pet was born on {pet.birth_date}. "
    if pet.weight:
        prompt += f"The pet weighs {pet.weight} kg. "
    if pet.behavior_issues:
        prompt += f"The known behavior issues are: {', '.join(pet.behavior_issues)}."

    response = _call_gemini(prompt)
    return response


@router.post("/gemini/health")
def generate_health_advice(pet: Pet):
    """
    Provides health advice for a pet based on its breed, age, weight, and known health issues.
    """
    if pet.breed == "other" and not pet.other_breed:
        raise HTTPException(status_code=400, detail="other_breed is required when breed is 'other'.")

    breed_info = pet.other_breed if pet.breed == "other" else pet.breed
    prompt = f"Provide health advice for a {breed_info} {pet.type}. "
    if pet.birth_date:
        prompt += f"The pet was born on {pet.birth_date}. "
    if pet.weight:
        prompt += f"The pet weighs {pet.weight} kg. "
    if pet.health_issues:
        prompt += f"The known health issues are: {', '.join(pet.health_issues)}."

    response = _call_gemini(prompt)
    return response


def _call_gemini(prompt):
    """
    Helper function to call the GEMINI API.
    """
    try:
        headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
        response = httpx.post(
            GEMINI_API_URL,
            headers=headers,
            json={"prompt": prompt}
        )
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Gemini service error: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
