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

@router.get("/{reminder_id}/export")
def export_reminder_to_ics(reminder_id: int, db: Session = Depends(get_db)):
    try:
        reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
        if not reminder:
            raise HTTPException(status_code=404, detail="Reminder not found")

        ics_content = generate_ics(reminder)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ics") as temp_file:
            temp_file.write(ics_content.encode("utf-8"))
            temp_filepath = temp_file.name

        return {"message": "ICS file generated", "file_path": temp_filepath}
    except SQLAlchemyError as e:
        logger.error(f"Error exporting reminder to ICS: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred.")