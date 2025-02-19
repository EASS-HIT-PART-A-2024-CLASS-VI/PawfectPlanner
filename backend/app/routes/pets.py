from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from backend.app.schemas import PetCreate, PetUpdate, PetResponse
from backend.app.models import Pet as PetModel
from backend.app.database import get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=PetResponse)
def create_pet(pet: PetCreate, db: Session = Depends(get_db)):
    """
    Create a new pet profile.
    - Ensures `other_breed` is only used when breed is set to "other".
    - Handles database errors gracefully.
    """
    try:
        if pet.breed == "other" and not pet.other_breed:
            raise HTTPException(status_code=400, detail="When breed is 'other', other_breed must be provided.")

        if pet.breed != "other" and pet.other_breed:
            raise HTTPException(status_code=400, detail="other_breed should only be set if breed is 'other'.")

        new_pet = PetModel(**pet.dict())
        db.add(new_pet)
        db.commit()
        db.refresh(new_pet)
        return new_pet
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating pet: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred.")

@router.get("/{pet_id}", response_model=PetResponse)
def get_pet(pet_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a pet profile by ID.
    - Returns 404 if the pet does not exist.
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
    - Ensures `other_breed` is only used when breed is set to "other".
    - Returns 404 if the pet does not exist.
    - Handles database errors gracefully.
    """
    try:
        existing_pet = db.query(PetModel).filter(PetModel.id == pet_id).first()
        if not existing_pet:
            raise HTTPException(status_code=404, detail="Pet not found.")

        if pet.breed == "other" and not pet.other_breed:
            raise HTTPException(status_code=400, detail="When breed is 'other', other_breed must be provided.")

        if pet.breed != "other" and pet.other_breed:
            raise HTTPException(status_code=400, detail="other_breed should only be set if breed is 'other'.")

        for key, value in pet.dict(exclude_unset=True).items():
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
    - Returns 404 if the pet does not exist.
    - Handles database errors gracefully.
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
