import React, { useState, useEffect } from "react";
import "../styles/PetProfile.css";

const PetProfile = () => {
  const [name, setName] = useState("");
  const [type, setType] = useState("Dog");
  const [breed, setBreed] = useState("");
  const [breedOptions, setBreedOptions] = useState([]);
  const [age, setAge] = useState("");
  const [weight, setWeight] = useState("");
  const [healthIssues, setHealthIssues] = useState([]);
  const [behaviorIssues, setBehaviorIssues] = useState([]);
  const [issueInput, setIssueInput] = useState("");
  const [behaviorInput, setBehaviorInput] = useState("");

  useEffect(() => {
    fetch(`/api/breeds?type=${type}`)
      .then((res) => res.json())
      .then((data) => setBreedOptions(data))
      .catch((err) => console.error("Error fetching breeds:", err));
  }, [type]);

  const addHealthIssue = () => {
    if (issueInput) {
      setHealthIssues([...healthIssues, issueInput]);
      setIssueInput("");
    }
  };

  const addBehaviorIssue = () => {
    if (behaviorInput) {
      setBehaviorIssues([...behaviorIssues, behaviorInput]);
      setBehaviorInput("");
    }
  };

  return (
    <div className="pet-profile-container">
      <h2 className="pet-profile-title">Enter Pet Profile</h2>

      <div className="form-group">
        <label>Pet Name:</label>
        <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
      </div>

      <div className="form-group">
        <label>Pet Type:</label>
        <select value={type} onChange={(e) => setType(e.target.value)}>
          <option value="Dog">Dog</option>
          <option value="Cat">Cat</option>
        </select>
      </div>

      <div className="form-group">
        <label>Breed:</label>
        <select value={breed} onChange={(e) => setBreed(e.target.value)}>
          {breedOptions.map((b) => (
            <option key={b} value={b}>{b}</option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label>Age (years):</label>
        <input type="number" value={age} onChange={(e) => setAge(e.target.value)} />
      </div>

      <div className="form-group">
        <label>Weight (kg):</label>
        <input type="number" value={weight} onChange={(e) => setWeight(e.target.value)} />
      </div>

      <div className="form-group">
        <label>Health Issues:</label>
        <input type="text" value={issueInput} onChange={(e) => setIssueInput(e.target.value)} />
        <button onClick={addHealthIssue}>Add</button>
        <ul className="health-issues-list">
          {healthIssues.map((issue, index) => (
            <li key={index} className="health-issue-item">{issue} ❌</li>
          ))}
        </ul>
      </div>

      <div className="form-group">
        <label>Behavior Issues:</label>
        <input type="text" value={behaviorInput} onChange={(e) => setBehaviorInput(e.target.value)} />
        <button onClick={addBehaviorIssue}>Add</button>
        <ul className="behavior-issues-list">
          {behaviorIssues.map((issue, index) => (
            <li key={index} className="behavior-issue-item">{issue} ❌</li>
          ))}
        </ul>
      </div>

      <button>Save Profile</button>
    </div>
  );
};

export default PetProfile;
