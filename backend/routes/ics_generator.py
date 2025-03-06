# File: backend/ics_generator.py
from ics import Calendar, Event
from datetime import timedelta

def generate_ics(reminder):
    """
    Generate an ICS file content from a reminder object.
    Assumes reminder has attributes:
      - title
      - due_date (a datetime object)
      - repeat (string, e.g., "2 days" or "once")
      - location (optional)
      - notes (optional, stored in description)
    """
    cal = Calendar()
    event = Event()
    event.name = reminder.title
    # Format the datetime in ICS standard (e.g., "YYYYMMDDTHHMMSS")
    event.begin = reminder.due_date.strftime("%Y%m%dT%H%M%S")
    if hasattr(reminder, "location") and reminder.location:
        event.location = reminder.location
    if hasattr(reminder, "notes") and reminder.notes:
        event.description = reminder.notes
    if hasattr(reminder, "repeat") and reminder.repeat and reminder.repeat.lower() != "once":
        parts = reminder.repeat.split()
        if len(parts) == 2:
            try:
                interval = int(parts[0])
            except ValueError:
                interval = 1  # default to 1 if parsing fails
            unit = parts[1].lower()
            if unit == "hours":
                event.duration = timedelta(hours=interval)
            elif unit == "days":
                event.duration = timedelta(days=interval)
            elif unit == "weeks":
                event.duration = timedelta(weeks=interval)
            elif unit == "months":
                event.duration = timedelta(days=interval * 30)
            elif unit == "years":
                event.duration = timedelta(days=interval * 365)
    cal.events.add(event)
    return cal.serialize()
