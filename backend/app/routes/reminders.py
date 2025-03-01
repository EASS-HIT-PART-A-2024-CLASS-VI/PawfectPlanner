from fastapi import APIRouter, HTTPException
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz
import uuid

router = APIRouter()

def generate_ics_event(title: str, description: str, date: str, frequency: str = None):
    """
    Generate an ICS file for reminders, ensuring compatibility with Outlook & mobile.
    - `title`: Event title.
    - `description`: Event details.
    - `date`: Event start date (YYYY-MM-DD).
    - `frequency`: Recurring frequency (e.g., "3 months" for vaccines).
    """
    try:
        event_date = datetime.strptime(date, "%Y-%m-%d")
        timezone = pytz.timezone("UTC")  # Ensure all timestamps use UTC

        cal = Calendar()
        cal.add("VERSION", "2.0")
        cal.add("PRODID", "-//PawfectPlanner//ICS Generator//EN")

        event = Event()
        event.add("SUMMARY", title)
        event.add("DESCRIPTION", description)
        event.add("DTSTART", event_date.replace(tzinfo=timezone))
        event.add("DTEND", event_date.replace(tzinfo=timezone) + timedelta(hours=1))  # Default: 1-hour duration
        event.add("DTSTAMP", datetime.now(timezone))
        event.add("UID", f"{uuid.uuid4()}@pawfectplanner.com")

        # **Add Recurrence Rule (RRULE) if frequency is provided**
        if frequency:
            freq_parts = frequency.split()
            if len(freq_parts) == 2 and freq_parts[1].lower() in ["days", "weeks", "months", "years"]:
                interval = freq_parts[0]
                freq_map = {"days": "DAILY", "weeks": "WEEKLY", "months": "MONTHLY", "years": "YEARLY"}
                event.add("RRULE", {"FREQ": freq_map[freq_parts[1]], "INTERVAL": interval})

        cal.add_component(event)

        return cal.to_ical()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating ICS: {str(e)}")

@router.get("/reminders/download")
def download_reminder(title: str, description: str, date: str, frequency: str = None):
    """
    API to generate an ICS reminder download.
    - Example: `/reminders/download?title=Vet Visit&description=Annual checkup&date=2025-06-01`
    - Supports recurrence: `/reminders/download?title=Worm Vaccine&date=2025-06-01&frequency=3 months`
    """
    ics_content = generate_ics_event(title, description, date, frequency)
    return {
        "filename": f"{title.replace(' ', '_')}.ics",
        "content": ics_content.decode("utf-8"),
    }