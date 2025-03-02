import os
import requests
import logging
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.schemas import PetCreate, PetUpdate, PetResponse
from app.models import Pet as PetModel
from app.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter()

DOG_API_URL = os.getenv("DOG_API_URL", "https://api.thedogapi.com/v1/breeds")
DOG_API_KEY = os.getenv("DOG_API_KEY")


def get_breed_info(breed_name: str):
    """
    Fetch breed details from The Dog API based on breed name.
    Returns average weight, life expectancy, temperament, and health issues.
    """
    headers = {"x-api-key": DOG_API_KEY}
    response = requests.get(DOG_API_URL, headers=headers)

    if response.status_code != 200:
        logger.error("Error fetching breed data from The Dog API.")
        return None

    breeds = response.json()
    for breed in breeds:
        if breed["name"].lower() == breed_name.lower():
            return {
                "average_weight": breed["weight"]["metric"],
                "life_expectancy": breed["life_span"],
                "temperament": breed.get("temperament", "Unknown"),
                "health_issues": breed.get("bred_for", "Unknown"),
            }
    return None


@router.get("/", response_model=List[PetResponse])
def list_pets(db: Session = Depends(get_db)):
    """
    Return all pets in the database.
    Used by the Dashboard to show the pet list.
    """
    try:
        pets = db.query(PetModel).all()
        return pets
    except SQLAlchemyError as e:
        logger.error(f"Error fetching pets: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred.")


@router.post("/", response_model=PetResponse)
def create_pet(pet: PetCreate, db: Session = Depends(get_db)):
    """
    Create a new pet profile.
    """
    try:
        if pet.breed == "other" and not pet.other_breed:
            raise HTTPException(
                status_code=400,
                detail="When breed is 'other', other_breed must be provided.",
            )
        if pet.breed != "other" and pet.other_breed:
            raise HTTPException(
                status_code=400,
                detail="other_breed should only be set if breed is 'other'.",
            )

        breed_info = get_breed_info(pet.breed) if pet.breed != "other" else None

        new_pet = PetModel(
            name=pet.name,
            breed=pet.breed,
            other_breed=pet.other_breed,
            weight=pet.weight,
            birth_date=pet.birth_date,
            type=pet.type,
        )
        db.add(new_pet)
        db.commit()
        db.refresh(new_pet)

        # If you want to store breed info in the DB, you'll need columns for it.
        # Or you can attach it to the response, e.g. new_pet.breed_info = breed_info

        return new_pet

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating pet: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred.")


@router.get("/{pet_id}", response_model=PetResponse)
def get_pet(pet_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a pet profile by ID, including breed details if available.
    """
    try:
        pet = db.query(PetModel).filter(PetModel.id == pet_id).first()
        if not pet:
            raise HTTPException(status_code=404, detail="Pet not found.")
        return pet

    except SQLAlchemyError as e:
        logger.error(f"Error retrieving pet: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred.")


@router.put("/{pet_id}", response_model=PetResponse)
def update_pet(pet_id: int, pet: PetUpdate, db: Session = Depends(get_db)):
    """
    Update an existing pet profile.
    """
    try:
        existing_pet = db.query(PetModel).filter(PetModel.id == pet_id).first()
        if not existing_pet:
            raise HTTPException(status_code=404, detail="Pet not found.")

        if pet.breed == "other" and not pet.other_breed:
            raise HTTPException(
                status_code=400,
                detail="When breed is 'other', other_breed must be provided.",
            )
        if pet.breed != "other" and pet.other_breed:
            raise HTTPException(
                status_code=400,
                detail="other_breed should only be set if breed is 'other'.",
            )

        data = pet.dict(exclude_unset=True)

        # If breed changed, we could re-fetch breed info here if you store it
        # For now, just set the fields
        for key, value in data.items():
            setattr(existing_pet, key, value)

        db.commit()
        db.refresh(existing_pet)
        return existing_pet

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error updating pet: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred.")


@router.delete("/{pet_id}")
def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    """
    Delete a pet profile by ID.
    """
    try:
        pet = db.query(PetModel).filter(PetModel.id == pet_id).first()
        if not pet:
            raise HTTPException(status_code=404, detail="Pet not found.")

        db.delete(pet)
        db.commit()
        return {"message": "Pet deleted successfully"}

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error deleting pet: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred.")
