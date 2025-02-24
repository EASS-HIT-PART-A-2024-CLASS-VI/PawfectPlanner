from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models import Reminder
from app.schemas import ReminderCreate, ReminderUpdate, ReminderResponse
from app.database import get_db
import logging
from ics import Calendar, Event
import datetime
import tempfile

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=ReminderResponse)
def create_reminder(reminder: ReminderCreate, db: Session = Depends(get_db)):
    """
    Create a new reminder.
    - Handles database errors gracefully.
    """
    try:
        db_reminder = Reminder(**reminder.dict())
        db.add(db_reminder)
        db.commit()
        db.refresh(db_reminder)
        return db_reminder
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating reminder: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred.")


@router.get("/{reminder_id}", response_model=ReminderResponse)
def get_reminder(reminder_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific reminder by ID.
    - Returns 404 if the reminder does not exist.
    """
    try:
        reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
        if not reminder:
            raise HTTPException(status_code=404, detail="Reminder not found")
        return reminder
    except SQLAlchemyError as e:
        logger.error(f"Error retrieving reminder: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred.")


@router.put("/{reminder_id}", response_model=ReminderResponse)
def update_reminder(reminder_id: int, reminder_update: ReminderUpdate, db: Session = Depends(get_db)):
    """
    Update an existing reminder.
    - Returns 404 if the reminder does not exist.
    - Handles database errors gracefully.
    """
    try:
        reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
        if not reminder:
            raise HTTPException(status_code=404, detail="Reminder not found")

        for key, value in reminder_update.dict(exclude_unset=True).items():
            setattr(reminder, key, value)

        db.commit()
        db.refresh(reminder)
        return reminder
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error updating reminder: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred.")


@router.delete("/{reminder_id}")
def delete_reminder(reminder_id: int, db: Session = Depends(get_db)):
    """
    Delete a reminder.
    - Returns 404 if the reminder does not exist.
    - Handles database errors gracefully.
    """
    try:
        reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
        if not reminder:
            raise HTTPException(status_code=404, detail="Reminder not found")

        db.delete(reminder)
        db.commit()
        return {"message": "Reminder deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error deleting reminder: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred.")


@router.get("/{reminder_id}/export")
def export_reminder_to_ics(reminder_id: int, db: Session = Depends(get_db)):
    """
    Export a reminder to an .ics file for calendar integration.
    - Returns 404 if the reminder does not exist.
    - Uses a temporary file for better file handling.
    """
    try:
        reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
        if not reminder:
            raise HTTPException(status_code=404, detail="Reminder not found")

        # Create an ICS calendar event
        calendar = Calendar()
        event = Event()
        event.name = reminder.title
        event.description = reminder.description or "No description provided."
        event.begin = reminder.due_date.isoformat()
        calendar.events.add(event)

        # Save the file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ics") as temp_file:
            temp_file.writelines(calendar.serialize().encode("utf-8"))
            temp_filepath = temp_file.name

        return {"message": "ICS file generated", "file_path": temp_filepath}
    except SQLAlchemyError as e:
        logger.error(f"Error exporting reminder to ICS: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred.")
