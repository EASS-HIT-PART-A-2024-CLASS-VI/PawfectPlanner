# File: backend/routes/pets.py
import os
import requests
import logging
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from schemas import PetCreate, PetUpdate, PetResponse
from models import Pet as PetModel
from database import get_db

# ✅ Import from our new cache module
from cache import get_json, set_json

logger = logging.getLogger(__name__)

DOG_SEARCH_URL = "https://api.thedogapi.com/v1/breeds/search?q="
CAT_SEARCH_URL = "https://api.thecatapi.com/v1/breeds/search?q="

DOG_API_KEY = os.getenv("DOG_API_KEY", "")
CAT_API_KEY = os.getenv("CAT_API_KEY", "")

router = APIRouter()

def fetch_breed_info(breed_name: str, pet_type: str):
    """
    Fetch breed details from The Dog API or The Cat API, 
    using Redis caching to avoid repeated calls.
    """
    if not breed_name:
        return None

    # Prepare a cache key, e.g. "breed_info:dog:french bulldog"
    cache_key = f"breed_info:{pet_type.lower()}:{breed_name.lower()}"

    # 1) Check Redis
    cached = get_json(cache_key)
    if cached:
        logger.info(f"[CACHE HIT] Breed info for {pet_type}/{breed_name} from Redis")
        return cached

    # 2) Not in cache, so do an external request
    breed_name = breed_name.lower()
    if pet_type.lower() == "dog":
        url = DOG_SEARCH_URL + breed_name
        headers = {"x-api-key": DOG_API_KEY} if DOG_API_KEY else {}
    elif pet_type.lower() == "cat":
        url = CAT_SEARCH_URL + breed_name
        headers = {"x-api-key": CAT_API_KEY} if CAT_API_KEY else {}
    else:
        return None

    try:
        resp = requests.get(url, headers=headers, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        if not data:
            return None

        breed_data = data[0]
        life_span = breed_data.get("life_span", "Unknown")
        life_span = life_span.replace("years", "").replace("Years", "").strip()
        if life_span and "Unknown" not in life_span:
            life_span += " years"

        # ✅ Log the raw API response
        logger.info(f"Breed API response for '{breed_name}': {data}")

        breed_info = {
            "average_weight_range": breed_data.get("weight", {}).get("metric", "Unknown"),
            "life_expectancy": life_span,
            "temperament": breed_data.get("temperament", "Unknown"),
            "bred_for": breed_data.get("bred_for"),
            "breed_group": breed_data.get("breed_group"),
        }

        # 3) Store in Redis for 24h
        set_json(cache_key, breed_info, expire_seconds=86400)

        return breed_info

    except (requests.RequestException, KeyError) as e:
        logger.error(f"Error fetching breed data: {e}")
        return None


@router.get("", response_model=List[PetResponse])
def list_pets(db: Session = Depends(get_db)):
    """Fetch all pets in the database."""
    return db.query(PetModel).all()


@router.post("", response_model=PetResponse)
def create_pet(pet_data: PetCreate, db: Session = Depends(get_db)):
    """Create a new pet."""
    logger.info(f"[CREATE PET] type={pet_data.type}, breed={pet_data.breed}, other_breed={pet_data.other_breed}")

    breed_info = None
    if pet_data.type and pet_data.breed and pet_data.type.lower() in ["dog", "cat"]:
        logger.info("[CREATE PET] fetch_breed_info will be called...")
        breed_info = fetch_breed_info(pet_data.breed, pet_data.type)
    else:
        logger.info("[CREATE PET] Skipping fetch_breed_info (type/breed condition not met)")

    health_issues_str = ",".join(pet_data.health_issues) if pet_data.health_issues else None
    behavior_issues_str = ",".join(pet_data.behavior_issues) if pet_data.behavior_issues else None

    new_pet = PetModel(
        name=pet_data.name,
        type=pet_data.type,
        breed=pet_data.breed,
        other_breed=pet_data.other_breed,
        birth_date=pet_data.birth_date,
        weight=pet_data.weight,
        health_issues=health_issues_str,
        behavior_issues=behavior_issues_str,
        owner_id=pet_data.owner_id
    )

    if breed_info:
        new_pet.average_weight_range = breed_info["average_weight_range"] or "Unknown"
        new_pet.life_expectancy = breed_info["life_expectancy"] or "Unknown"
        new_pet.temperament = breed_info["temperament"] or "Unknown"
        new_pet.bred_for = breed_info["bred_for"]
        new_pet.breed_group = breed_info["breed_group"]

    try:
        db.add(new_pet)
        db.commit()
        db.refresh(new_pet)
        return new_pet
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating pet: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create pet.")


@router.get("/{pet_id}", response_model=PetResponse)
def get_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(PetModel).filter(PetModel.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet


@router.delete("/{pet_id}")
def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(PetModel).filter(PetModel.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    db.delete(pet)
    db.commit()
    return {"detail": "Pet deleted successfully"}


@router.put("/{pet_id}", response_model=PetResponse)
def update_pet(pet_id: int, pet_data: PetUpdate, db: Session = Depends(get_db)):
    pet = db.query(PetModel).filter(PetModel.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    logger.info(f"[UPDATE PET] type={pet_data.type}, breed={pet_data.breed}, other_breed={pet_data.other_breed}")

    if pet_data.type and pet_data.breed and pet_data.type.lower() in ["dog", "cat"]:
        logger.info("[UPDATE PET] fetch_breed_info will be called...")
        breed_info = fetch_breed_info(pet_data.breed, pet_data.type)
        if breed_info:
            pet.average_weight_range = breed_info["average_weight_range"] or "Unknown"
            pet.life_expectancy = breed_info["life_expectancy"] or "Unknown"
            pet.temperament = breed_info["temperament"] or "Unknown"
            pet.bred_for = breed_info["bred_for"]
            pet.breed_group = breed_info["breed_group"]
    else:
        logger.info("[UPDATE PET] Skipping fetch_breed_info (type/breed condition not met)")

    if pet_data.name is not None:
        pet.name = pet_data.name
    if pet_data.type is not None:
        pet.type = pet_data.type
    if pet_data.breed is not None:
        pet.breed = pet_data.breed
    if pet_data.other_breed is not None:
        pet.other_breed = pet_data.other_breed
    if pet_data.birth_date is not None:
        pet.birth_date = pet_data.birth_date
    if pet_data.weight is not None:
        pet.weight = pet_data.weight
    if pet_data.health_issues is not None:
        pet.health_issues = ",".join(pet_data.health_issues) if pet_data.health_issues else None
    if pet_data.behavior_issues is not None:
        pet.behavior_issues = ",".join(pet_data.behavior_issues) if pet_data.behavior_issues else None

    try:
        db.commit()
        db.refresh(pet)
        return pet
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error updating pet: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update pet.")
