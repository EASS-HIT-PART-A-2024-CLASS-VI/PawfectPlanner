// File: frontend/src/pages/Reminders.jsx
import React, { useState, useEffect } from "react";
import axiosInstance from "../services/axiosSetup";
import "../styles/Reminders.css";

function Reminders() {
  const [title, setTitle] = useState("");
  const [date, setDate] = useState("");
  const [time, setTime] = useState("");
  const [repetition, setRepetition] = useState("once");
  const [repeatInterval, setRepeatInterval] = useState(1);
  const [location, setLocation] = useState("");
  const [notes, setNotes] = useState("");
  const [petId, setPetId] = useState("");
  const [pets, setPets] = useState([]);
  const [reminders, setReminders] = useState([]);

  useEffect(() => {
    fetchReminders();
    fetchPets();
  }, []);

  const fetchReminders = async () => {
    try {
      const res = await axiosInstance.get("/reminders");
      setReminders(res.data);
    } catch (error) {
      console.error("Error fetching reminders:", error);
    }
  };

  const fetchPets = async () => {
    try {
      const res = await axiosInstance.get("/pets");
      setPets(res.data);
    } catch (error) {
      console.error("Error fetching pets:", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    let finalRepetition = "once";
    if (repetition !== "once") {
      finalRepetition = `${repeatInterval} ${repetition}`;
    }

    const payload = {
      title,
      date,
      time,
      repetition: finalRepetition,
      location,
      notes,
      pet_id: petId ? parseInt(petId, 10) : null,
    };

    try {
      await axiosInstance.post("/reminders", payload);
      alert("Reminder created successfully!");
      setTitle("");
      setDate("");
      setTime("");
      setRepetition("once");
      setRepeatInterval(1);
      setLocation("");
      setNotes("");
      setPetId("");
      fetchReminders();
    } catch (err) {
      console.error("Error creating reminder:", err);
      alert("Could not create reminder. Check console for details.");
    }
  };

  // Helper to format ISO date/time
  const formatDueDate = (isoString) => {
    const dateObj = new Date(isoString);
    if (isNaN(dateObj.getTime())) return isoString; // fallback if invalid

    return dateObj.toLocaleString([], {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      hour12: false,
    });
  };

  const handleDownloadICS = (reminderId) => {
    window.open(`/api/reminders/download/${reminderId}`, "_blank");
  };

  const handleDelete = async (reminderId) => {
    if (!window.confirm("Are you sure you want to delete this reminder?")) return;
    try {
      await axiosInstance.delete(`/reminders/${reminderId}`);
      alert("Reminder deleted.");
      fetchReminders();
    } catch (err) {
      console.error("Error deleting reminder:", err);
      alert("Could not delete reminder.");
    }
  };

  return (
    <div className="reminders-container">
      <h2>Pet Care Reminders</h2>
      <form onSubmit={handleSubmit}>
        <div className="reminder-field">
          <label>Title *</label>
          <input
            type="text"
            value={title}
            required
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>

        <div className="reminder-field">
          <label>Date *</label>
          <input
            type="date"
            value={date}
            required
            onChange={(e) => setDate(e.target.value)}
          />
        </div>

        <div className="reminder-field">
          <label>Time *</label>
          <input
            type="time"
            value={time}
            required
            onChange={(e) => setTime(e.target.value)}
          />
        </div>

        <div className="reminder-field">
          <label>Repetition</label>
          <select
            value={repetition}
            onChange={(e) => setRepetition(e.target.value)}
          >
            <option value="once">Once</option>
            <option value="hours">Every X Hours</option>
            <option value="days">Every X Days</option>
            <option value="weeks">Every X Weeks</option>
            <option value="months">Every X Months</option>
            <option value="years">Every X Years</option>
          </select>
          {repetition !== "once" && (
            <div style={{ marginTop: "0.3rem" }}>
              <label style={{ marginRight: "0.5rem" }}>Interval:</label>
              <input
                type="number"
                min="1"
                value={repeatInterval}
                onChange={(e) => setRepeatInterval(e.target.value)}
                style={{ width: "60px" }}
              />
            </div>
          )}
        </div>

        <div className="reminder-field">
          <label>Location (Optional)</label>
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          />
        </div>

        <div className="reminder-field">
          <label>Notes (Optional)</label>
          <input
            type="text"
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
          />
        </div>

        <div className="reminder-field">
          <label>Pet (Optional)</label>
          <select
            value={petId}
            onChange={(e) => setPetId(e.target.value)}
          >
            <option value="">No Pet</option>
            {pets.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name} ({p.breed})
              </option>
            ))}
          </select>
        </div>

        <button type="submit">Add Reminder</button>
      </form>

      <h3>Existing Reminders</h3>
      {reminders.length === 0 ? (
        <p>No reminders found. Add one above!</p>
      ) : (
        <ul className="reminder-list">
          {reminders.map((r) => {
            const niceDate = formatDueDate(r.due_date);
            return (
              <li className="reminder-item" key={r.id}>
                {/* 1) text block */}
                <div className="reminder-text">
                  <strong>{r.title}</strong> | Due: {niceDate} | Repeat: {r.repetition}
                </div>
                {/* 2) button block */}
                <div className="reminder-buttons">
                  <button onClick={() => handleDownloadICS(r.id)}>Add to Calendar</button>
                  <button onClick={() => handleDelete(r.id)}>Delete</button>
                </div>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}

export default Reminders;
