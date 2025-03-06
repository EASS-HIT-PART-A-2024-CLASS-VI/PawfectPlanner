# File: backend/routes/reminders.py
from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import pytz
import uuid
from icalendar import Calendar, Event

from database import get_db
from models import Reminder, Pet
from schemas import ReminderCreate, ReminderResponse

router = APIRouter()

@router.get("", response_model=list[ReminderResponse])
def list_reminders(db: Session = Depends(get_db)):
    """
    Fetch all reminders + optionally the pet name if available.
    """
    results = (
        db.query(Reminder, Pet.name.label("pet_name"))
        .outerjoin(Pet, Pet.id == Reminder.pet_id)
        .all()
    )

    reminder_list = []
    for (rem, pet_name) in results:
        # If there's a pet name, append it to the reminder title
        reminder_list.append(
            ReminderResponse(
                id=rem.id,
                pet_id=rem.pet_id,
                title=f"{rem.title} (for {pet_name})" if pet_name else rem.title,
                due_date=rem.due_date,
                repetition=rem.repeat if rem.repeat else "once",
                location=rem.location,
                notes=rem.description,
            )
        )
    return reminder_list

@router.post("", response_model=ReminderResponse)
def create_reminder(reminder_data: ReminderCreate, db: Session = Depends(get_db)):
    """
    Create a new reminder.
    """
    try:
        # Combine date + time into a single datetime
        due_datetime = datetime.strptime(
            f"{reminder_data.date} {reminder_data.time}", "%Y-%m-%d %H:%M"
        )
        repeat_val = reminder_data.repetition.lower()
        if repeat_val == "once":
            repeat_val = "once"

        new_reminder = Reminder(
            title=reminder_data.title,
            due_date=due_datetime,
            repeat=repeat_val,
            description=reminder_data.notes or "",
            location=reminder_data.location,
            pet_id=reminder_data.pet_id
        )
        db.add(new_reminder)
        db.commit()
        db.refresh(new_reminder)
        return ReminderResponse(
            id=new_reminder.id,
            pet_id=new_reminder.pet_id,
            title=new_reminder.title,
            due_date=new_reminder.due_date,
            repetition=new_reminder.repeat,
            location=new_reminder.location,
            notes=new_reminder.description
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add reminder: {str(e)}")

@router.get("/download/{reminder_id}")
def download_reminder(reminder_id: int, db: Session = Depends(get_db)):
    """
    Download a reminder as ICS, including pet name if available.
    """
    rem = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not rem:
        raise HTTPException(status_code=404, detail="Reminder not found")

    pet_name = None
    if rem.pet_id:
        pet = db.query(Pet).filter(Pet.id == rem.pet_id).first()
        if pet:
            pet_name = pet.name

    try:
        ics_content = generate_ics_event(rem, pet_name)
        return Response(
            content=ics_content,
            media_type="text/calendar",
            headers={
                "Content-Disposition": f"attachment; filename=reminder_{rem.id}.ics"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating ICS: {str(e)}")

@router.delete("/{reminder_id}")
def delete_reminder(reminder_id: int, db: Session = Depends(get_db)):
    """
    Delete a reminder by ID.
    """
    rem = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not rem:
        raise HTTPException(status_code=404, detail="Reminder not found.")
    db.delete(rem)
    db.commit()
    return {"detail": "Reminder deleted successfully."}

def generate_ics_event(reminder: Reminder, pet_name: str = None):
    """
    Helper to build ICS data for a given reminder.
    """
    timezone = pytz.UTC
    cal = Calendar()
    cal.add("VERSION", "2.0")
    cal.add("PRODID", "-//PawfectPlanner//Reminders//EN")

    event = Event()
    summary = reminder.title
    if pet_name:
        summary += f" (for {pet_name})"

    event.add("SUMMARY", summary)
    event.add("DESCRIPTION", reminder.description or "")
    if reminder.location:
        event.add("LOCATION", reminder.location)
    event.add("DTSTART", reminder.due_date.replace(tzinfo=timezone))
    event.add("DTEND", (reminder.due_date + timedelta(hours=1)).replace(tzinfo=timezone))
    event.add("DTSTAMP", datetime.now(timezone))
    event.add("UID", f"{uuid.uuid4()}@pawfectplanner.com")

    if reminder.repeat and reminder.repeat.lower() != "once":
        parts = reminder.repeat.split()
        if len(parts) == 2:
            interval, unit = parts
            freq_map = {
                "hours": "HOURLY",
                "days": "DAILY",
                "weeks": "WEEKLY",
                "months": "MONTHLY",
                "years": "YEARLY",
            }
            if unit.lower() in freq_map:
                event.add("RRULE", {"FREQ": freq_map[unit.lower()], "INTERVAL": interval})

    cal.add_component(event)
    return cal.to_ical()
