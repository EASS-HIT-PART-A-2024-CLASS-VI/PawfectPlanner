from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.app.models import Treatment
from backend.app.schemas import TreatmentCreate, TreatmentUpdate, TreatmentResponse
from backend.app.database import get_db
from typing import List
import os
from ics import Calendar, Event
import datetime

router = APIRouter()


@router.post("/pets/{pet_id}/treatments", response_model=TreatmentResponse)
def create_treatment(pet_id: int, treatment: TreatmentCreate, db: Session = Depends(get_db)):
    """
    Create a new treatment for a specific pet.
    """
    new_treatment = Treatment(**treatment.model_dump(), pet_id=pet_id)
    db.add(new_treatment)
    db.commit()
    db.refresh(new_treatment)
    return new_treatment


@router.get("/pets/{pet_id}/treatments", response_model=List[TreatmentResponse])
def get_treatments(pet_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all treatments for a given pet.
    """
    treatments = db.query(Treatment).filter(Treatment.pet_id == pet_id).all()
    return treatments


@router.put("/pets/{pet_id}/treatments/{treatment_id}", response_model=TreatmentResponse)
def update_treatment(pet_id: int, treatment_id: int, treatment_update: TreatmentUpdate, db: Session = Depends(get_db)):
    """
    Update a specific treatment for a pet.
    """
    treatment = db.query(Treatment).filter(Treatment.id == treatment_id, Treatment.pet_id == pet_id).first()
    if not treatment:
        raise HTTPException(status_code=404, detail="Treatment not found")

    for key, value in treatment_update.model_dump(exclude_unset=True).items():
        setattr(treatment, key, value)

    db.commit()
    db.refresh(treatment)
    return treatment


@router.delete("/pets/{pet_id}/treatments/{treatment_id}")
def delete_treatment(pet_id: int, treatment_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific treatment for a pet.
    """
    treatment = db.query(Treatment).filter(Treatment.id == treatment_id, Treatment.pet_id == pet_id).first()
    if not treatment:
        raise HTTPException(status_code=404, detail="Treatment not found")

    db.delete(treatment)
    db.commit()
    return {"detail": "Treatment deleted"}


@router.get("/pets/{pet_id}/treatments/{treatment_id}/export")
def export_treatment_to_ics(pet_id: int, treatment_id: int, db: Session = Depends(get_db)):
    """
    Export a treatment schedule as an .ics file for calendar integration.
    """
    treatment = db.query(Treatment).filter(Treatment.id == treatment_id, Treatment.pet_id == pet_id).first()
    if not treatment:
        raise HTTPException(status_code=404, detail="Treatment not found")

    # Create an ICS calendar event
    calendar = Calendar()
    event = Event()
    event.name = treatment.name
    event.description = treatment.description
    event.begin = treatment.due_date.isoformat() if treatment.due_date else datetime.datetime.now().isoformat()
    calendar.events.add(event)

    # Save the file to a temporary location
    filename = f"treatment_{treatment_id}.ics"
    filepath = os.path.join("/tmp", filename)
    with open(filepath, "w") as file:
        file.writelines(calendar.serialize())

    return {"detail": f"ICS file created at {filepath}"}
