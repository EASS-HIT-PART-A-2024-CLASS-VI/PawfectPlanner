// src/pages/Reminders.jsx
import React, { useState, useEffect } from "react";
import axios from "axios";
import FileSaver from "file-saver";
import { API_BASE_URL } from "../config";
import "./styles/Reminders.css";

const Reminders = () => {
  const [reminder, setReminder] = useState("");
  const [date, setDate] = useState("");
  const [time, setTime] = useState("");
  const [repeatType, setRepeatType] = useState("Once");
  const [repeatValue, setRepeatValue] = useState(1);
  const [location, setLocation] = useState("");
  const [notes, setNotes] = useState("");
  const [reminders, setReminders] = useState([]);

  useEffect(() => {
    fetchReminders();
  }, []);

  const fetchReminders = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/reminders`);
      setReminders(response.data);
    } catch (error) {
      console.error("Failed to fetch reminders:", error);
    }
  };

  const addReminder = async () => {
    if (!reminder || !date || !time) {
      alert("Please fill in all required fields.");
      return;
    }

    const newReminder = {
      reminder,
      date,
      time,
      repeat: repeatType !== "Once" ? `${repeatValue} ${repeatType}` : "Once",
      location,
      notes,
    };

    try {
      await axios.post(`${API_BASE_URL}/reminders`, newReminder);
      fetchReminders();
      setReminder("");
      setDate("");
      setTime("");
      setRepeatType("Once");
      setRepeatValue(1);
      setLocation("");
      setNotes("");
    } catch (error) {
      console.error("Failed to add reminder:", error);
    }
  };

  return (
    <div className="reminders-page">
      <h2>Pet Care Reminders</h2>
      <input type="text" placeholder="Reminder" value={reminder} onChange={(e) => setReminder(e.target.value)} />
      <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
      <input type="time" value={time} onChange={(e) => setTime(e.target.value)} />
      
      <div>
        <select value={repeatType} onChange={(e) => setRepeatType(e.target.value)}>
          <option value="Once">Once</option>
          <option value="hours">Every X hours</option>
          <option value="days">Every X days</option>
          <option value="weeks">Every X weeks</option>
          <option value="months">Every X months</option>
          <option value="years">Every X years</option>
        </select>
        {repeatType !== "Once" && (
          <input type="number" min="1" value={repeatValue} onChange={(e) => setRepeatValue(e.target.value)} />
        )}
      </div>
      
      <input type="text" placeholder="Location (Optional)" value={location} onChange={(e) => setLocation(e.target.value)} />
      <textarea placeholder="Notes (Optional)" value={notes} onChange={(e) => setNotes(e.target.value)} />
      <button onClick={addReminder}>Add Reminder</button>

      {reminders.map((r, index) => (
        <div key={index} className="reminder-item">
          <p><b>{r.reminder}</b> - {r.date} at {r.time} ({r.repeat})</p>
          {r.location && <p><b>Location:</b> {r.location}</p>}
          {r.notes && <p><b>Notes:</b> {r.notes}</p>}
        </div>
      ))}
    </div>
  );
};

export default Reminders;