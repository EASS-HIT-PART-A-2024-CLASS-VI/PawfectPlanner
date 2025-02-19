import { useState } from "react";
const ics = await import("ics");
const { createEvent } = ics;


function Reminders() {
  const [reminder, setReminder] = useState("");
  const [calendarLink, setCalendarLink] = useState(null);

  const handleGenerateICS = () => {
    const event = {
      title: reminder,
      start: [2025, 2, 4, 12, 0], // Example: Feb 4, 2025, at 12:00 PM
      duration: { minutes: 30 },
    };

    createEvent(event, (error, value) => {
      if (error) {
        console.log(error);
        return;
      }
      const file = new Blob([value], { type: "text/calendar" });
      setCalendarLink(URL.createObjectURL(file));
    });
  };

  return (
    <div>
      <h2>Pet Care Reminders</h2>
      <input
        type="text"
        value={reminder}
        onChange={(e) => setReminder(e.target.value)}
        placeholder="Enter reminder"
      />
      <button onClick={handleGenerateICS}>Add Reminder</button>
      {calendarLink && (
        <a href={calendarLink} download="reminder.ics">
          Download Reminder
        </a>
      )}
    </div>
  );
}

export default Reminders;
