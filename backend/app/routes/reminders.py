# File: backend/app/routes/reminders.py

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
import pytz
import uuid

from icalendar import Calendar, Event
from app.database import get_db
from app.models import Reminder

router = APIRouter()  # <--- removed prefix="/reminders"

@router.get("")
def list_reminders(db: Session = Depends(get_db)):
    """
    List all reminders from the DB, returning them in the shape the front end expects:
    { reminder, date, time, repeat, location, notes }.
    Currently storing everything except date/time in 'description'.
    """
    try:
        all_reminders = db.query(Reminder).all()
        results = []
        for r in all_reminders:
            date_str = r.due_date.strftime("%Y-%m-%d") if r.due_date else ""
            time_str = r.due_date.strftime("%H:%M") if r.due_date else ""
            results.append({
                "reminder": r.title,
                "date": date_str,
                "time": time_str,
                "repeat": "Once",
                "location": "",
                "notes": r.description or "",
            })
        return results
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

@router.post("")
def create_reminder(data: dict, db: Session = Depends(get_db)):
    """
    Create a new reminder in the DB.
    Expects a body like:
    {
      "reminder": "title",
      "date": "YYYY-MM-DD",
      "time": "HH:MM",
      "repeat": "Once" or "3 days" etc.,
      "location": "...",
      "notes": "..."
    }
    We'll store location/repeat/notes in 'description'.
    """
    try:
        if "reminder" not in data or "date" not in data or "time" not in data:
            raise HTTPException(status_code=400, detail="Missing required fields")

        date_str = data["date"]
        time_str = data["time"]
        try:
            dt_str = f"{date_str} {time_str}"
            due_datetime = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date/time format")

        title = data["reminder"]
        repeat = data.get("repeat", "Once")
        location = data.get("location", "")
        notes = data.get("notes", "")

        desc = f"{notes} | Location: {location} | Repeat: {repeat}"

        new_reminder = Reminder(
            title=title,
            description=desc,
            due_date=due_datetime
        )
        db.add(new_reminder)
        db.commit()
        db.refresh(new_reminder)

        return {
            "reminder": title,
            "date": date_str,
            "time": time_str,
            "repeat": repeat,
            "location": location,
            "notes": notes,
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

@router.get("/download")
def download_reminder(title: str, description: str, date: str, frequency: str = None):
    """
    Generate an ICS file for the specified reminder details.
    e.g. /api/reminders/download?title=Vet+Visit&description=Checkup&date=2025-06-01
    """
    ics_content = generate_ics_event(title, description, date, frequency)
    return {
        "filename": f"{title.replace(' ', '_')}.ics",
        "content": ics_content.decode("utf-8"),
    }

def generate_ics_event(title: str, description: str, date: str, frequency: str = None):
    try:
        event_date = datetime.strptime(date, "%Y-%m-%d")
        timezone = pytz.UTC

        cal = Calendar()
        cal.add("VERSION", "2.0")
        cal.add("PRODID", "-//PawfectPlanner//ICS Generator//EN")

        event = Event()
        event.add("SUMMARY", title)
        event.add("DESCRIPTION", description)

        start_dt = event_date.replace(tzinfo=timezone)
        end_dt = start_dt + timedelta(hours=1)

        event.add("DTSTART", start_dt)
        event.add("DTEND", end_dt)
        event.add("DTSTAMP", datetime.now(timezone))
        event.add("UID", f"{uuid.uuid4()}@pawfectplanner.com")

        if frequency:
            freq_parts = frequency.split()
            if len(freq_parts) == 2 and freq_parts[1].lower() in ["days", "weeks", "months", "years"]:
                interval = freq_parts[0]
                freq_map = {
                    "days": "DAILY",
                    "weeks": "WEEKLY",
                    "months": "MONTHLY",
                    "years": "YEARLY"
                }
                event.add("RRULE", {
                    "FREQ": freq_map[freq_parts[1].lower()],
                    "INTERVAL": interval
                })

        cal.add_component(event)
        return cal.to_ical()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"ICS generation error: {str(exc)}")
