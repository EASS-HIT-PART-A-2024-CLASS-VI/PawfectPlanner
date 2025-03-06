// File: frontend/src/pages/Treatments.jsx
import { useState } from "react";
import { saveAs } from "file-saver";
import "../styles/Treatments.css";

const vaccineData = {
  Dog: [
    {
      name: "Rabies",
      frequency: "Yearly",
      mandatory: true,
      description: "Protects against rabies, a fatal virus. Required by Israeli law.",
    },
    {
      name: "Hexavalent Vaccine",
      frequency: "Yearly",
      mandatory: true,
      description:
        "Protects against 6 major diseases: Distemper, Adenovirus, Parvovirus, Leptospirosis, Parainfluenza, and Coronavirus.",
    },
    {
      name: "Spirocerca Lupi (Park Worm) Prevention",
      frequency: "Every 3 months",
      mandatory: false,
      description: "Prevents infection by a parasitic worm common in Israel.",
    },
  ],
  Cat: [
    {
      name: "Rabies",
      frequency: "Yearly",
      mandatory: false,
      description: "Recommended for outdoor cats. Fatal if contracted.",
    },
    {
      name: "Quadrivalent Vaccine",
      frequency: "Yearly",
      mandatory: true,
      description:
        "Protects against Panleukopenia, Herpesvirus, Calicivirus, and Chlamydia.",
    },
    {
      name: "Feline Leukemia Virus (FeLV)",
      frequency: "Yearly",
      mandatory: false,
      description:
        "Recommended for outdoor cats to protect against immune system diseases.",
    },
  ],
};

const preventativeTreatments = {
  Dog: [
    {
      name: "Flea & Tick Prevention",
      frequency: "Monthly or as advised by vet",
      description:
        "Protects against fleas and ticks, preventing disease transmission (e.g., Ehrlichiosis from ticks).",
    },
    {
      name: "Internal Parasite Treatment",
      frequency: "Every 3-6 months",
      description: "Prevents intestinal worms (roundworms, tapeworms, hookworms).",
    },
  ],
  Cat: [
    {
      name: "Flea & Tick Prevention",
      frequency: "Monthly or as advised by vet",
      description:
        "Protects against fleas and ticks, which can cause allergic reactions and disease transmission (e.g., Hemobartonellosis).",
    },
    {
      name: "Internal Parasite Treatment",
      frequency: "Every 3-6 months",
      description:
        "Prevents intestinal worms causing weight loss, vomiting, and diarrhea.",
    },
  ],
};

// ICS generator
const generateICS = (treatment) => {
  const startDate = new Date();
  const formattedDate = startDate.toISOString().split("T")[0].replace(/-/g, "");

  const event = `BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
SUMMARY:${treatment.name} Treatment
DESCRIPTION:${treatment.description} - Frequency: ${treatment.frequency}
DTSTART:${formattedDate}T120000Z
END:VEVENT
END:VCALENDAR`;

  const blob = new Blob([event], { type: "text/calendar;charset=utf-8" });
  saveAs(blob, `${treatment.name.replace(/\s/g, "_")}.ics`);
};

function Treatments() {
  const [petType, setPetType] = useState("Dog");

  const addToCalendar = (item) => {
    generateICS(item);
  };

  return (
    <div className="treatments-container">
      <h2>Recommended Treatments</h2>
      <label>Pet Type:</label>
      <select value={petType} onChange={(e) => setPetType(e.target.value)}>
        <option value="Dog">Dog</option>
        <option value="Cat">Cat</option>
      </select>

      <h3>Vaccines:</h3>
      <ul className="vaccine-list">
        {vaccineData[petType].map((vaccine) => (
          <li key={vaccine.name} className="vaccine-item">
            <strong>{vaccine.name}</strong> ({vaccine.frequency}){" "}
            {vaccine.mandatory && <span className="mandatory">Mandatory</span>}
            <p>{vaccine.description}</p>
            <button
              className="download-btn"
              onClick={() => addToCalendar(vaccine)}
            >
              Add to Calendar
            </button>
          </li>
        ))}
      </ul>

      <h3>Preventative Treatments:</h3>
      <ul className="treatment-list">
        {preventativeTreatments[petType].map((treatment) => (
          <li key={treatment.name} className="treatment-item">
            <strong>{treatment.name}</strong> ({treatment.frequency})
            <p>{treatment.description}</p>
            <button
              className="download-btn"
              onClick={() => addToCalendar(treatment)}
            >
              Add to Calendar
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Treatments;
