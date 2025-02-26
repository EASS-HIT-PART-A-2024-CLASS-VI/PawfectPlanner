import { useState } from "react";
import { saveAs } from "file-saver";
import "../styles/Reminders.css";

const Reminders = () => {
  const [reminder, setReminder] = useState("");
  const [date, setDate] = useState("");
  const [time, setTime] = useState("");
  const [frequency, setFrequency] = useState("Once");
  const [reminders, setReminders] = useState([]);

  const addReminder = () => {
    if (reminder && date && time) {
      const newReminder = { reminder, date, time, frequency };
      setReminders([...reminders, newReminder]);
      setReminder("");
      setDate("");
      setTime("");
      setFrequency("Once");
    }
  };

  const generateICS = (reminder) => {
    const event = `BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
SUMMARY:${reminder.reminder}
DTSTART:${reminder.date.replace(/-/g, "")}T${reminder.time.replace(/:/g, "")}00Z
DESCRIPTION:Scheduled pet care reminder.
RRULE:FREQ=${reminder.frequency === "Daily" ? "DAILY" : reminder.frequency === "Weekly" ? "WEEKLY" : "NONE"}
END:VEVENT
END:VCALENDAR`;
    const blob = new Blob([event], { type: "text/calendar;charset=utf-8" });
    saveAs(blob, `${reminder.reminder.replace(/\s/g, "_")}.ics`);
  };

  return (
    <div className="reminders-container">
      <h2>Pet Care Reminders</h2>
      <input type="text" placeholder="Reminder" value={reminder} onChange={(e) => setReminder(e.target.value)} />
      <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
      <input type="time" value={time} onChange={(e) => setTime(e.target.value)} />
      <select value={frequency} onChange={(e) => setFrequency(e.target.value)}>
        <option value="Once">Once</option>
        <option value="Daily">Daily</option>
        <option value="Weekly">Weekly</option>
      </select>
      <button onClick={addReminder}>Add Reminder</button>

      <ul>
        {reminders.map((reminder, index) => (
          <li key={index}>
            {reminder.reminder} - {reminder.date} at {reminder.time} ({reminder.frequency})
            <button onClick={() => generateICS(reminder)}>Download ICS</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Reminders;
