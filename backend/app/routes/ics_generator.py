from ics import Calendar, Event
from datetime import datetime, timedelta

def generate_ics(reminder):
    cal = Calendar()
    event = Event()
    event.name = reminder.title
    event.begin = reminder.due_date.strftime("%Y%m%dT%H%M%S")

    if reminder.location:
        event.location = reminder.location

    if reminder.notes:
        event.description = reminder.notes

    if reminder.repeat and reminder.repeat != "Once":
        repeat_parts = reminder.repeat.split()
        interval = int(repeat_parts[0])
        unit = repeat_parts[1]
        
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