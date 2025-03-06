// File: frontend/src/pages/AddPet.jsx
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axiosInstance from "../services/axiosSetup";
import "../styles/AddPet.css";

function AddPet() {
  const navigate = useNavigate();

  const [userId, setUserId] = useState(null);
  const [name, setName] = useState("");
  const [type, setType] = useState("dog");
  const [breed, setBreed] = useState("");
  const [otherBreed, setOtherBreed] = useState("");
  const [breedSuggestions, setBreedSuggestions] = useState([]);
  const [birthDate, setBirthDate] = useState("");
  const [weight, setWeight] = useState("");
  const [healthIssues, setHealthIssues] = useState("");
  const [behaviorIssues, setBehaviorIssues] = useState("");

  useEffect(() => {
    axiosInstance
      .get("/auth/me")
      .then((res) => {
        setUserId(res.data.id);
      })
      .catch((err) => {
        console.error("No user or not logged in:", err);
      });
  }, []);

  const handleBreedSearch = async (query) => {
    if (type.toLowerCase() === "other") {
      setBreedSuggestions([]);
      return;
    }
    if (query.length < 3) {
      setBreedSuggestions([]);
      return;
    }
    try {
      const res = await axiosInstance.get(`/breeds/${type}/${query}`);
      if (Array.isArray(res.data)) {
        setBreedSuggestions(res.data);
      } else {
        setBreedSuggestions([res.data]);
      }
    } catch (err) {
      console.error("Error fetching breed suggestions:", err);
      setBreedSuggestions([]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!userId) {
      alert("Please log in first. No user ID found.");
      return;
    }
    if (!name.trim()) {
      alert("Pet name is required.");
      return;
    }

    try {
      const healthArr = healthIssues
        ? healthIssues.split(",").map((s) => s.trim())
        : [];
      const behaviorArr = behaviorIssues
        ? behaviorIssues.split(",").map((s) => s.trim())
        : [];

      const payload = {
        name,
        type,
        breed: type.toLowerCase() === "other" ? "other" : breed,
        other_breed: type.toLowerCase() === "other" ? otherBreed : null,
        birth_date: birthDate || null,
        weight: weight ? parseFloat(weight) : null,
        health_issues: healthArr,
        behavior_issues: behaviorArr,
        owner_id: userId,
      };

      const res = await axiosInstance.post("/pets", payload);
      alert("Pet created successfully!");
      navigate(`/profile/${res.data.id}`);
    } catch (err) {
      console.error("Error creating pet:", err);
      if (err.response && err.response.data) {
        const data = err.response.data;
        if (Array.isArray(data.detail)) {
          const messages = data.detail.map((item) => item.msg).join("\n");
          alert(`Validation Error:\n${messages}`);
        } else if (typeof data.detail === "string") {
          alert(`Error: ${data.detail}`);
        } else {
          alert("Could not create pet. Check console for details.");
        }
      } else {
        alert("Could not create pet. Check console for details.");
      }
    }
  };

  return (
    <div className="add-pet-container">
      <h2>Create a Pet Profile</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Name *</label>
          <input
            type="text"
            placeholder="e.g. Bob"
            value={name}
            required
            onChange={(e) => setName(e.target.value)}
          />
        </div>

        <div className="form-group">
          <label>Type *</label>
          <select
            value={type}
            onChange={(e) => {
              setType(e.target.value);
              setBreedSuggestions([]);
              setBreed("");
              setOtherBreed("");
            }}
          >
            <option value="dog">Dog</option>
            <option value="cat">Cat</option>
            <option value="other">Other</option>
          </select>
        </div>

        {type.toLowerCase() !== "other" && (
          <div className="form-group">
            <label>Breed</label>
            <div className="breed-input-wrapper">
              <input
                type="text"
                placeholder="e.g. German Shepherd"
                value={breed}
                onChange={(e) => {
                  setBreed(e.target.value);
                  handleBreedSearch(e.target.value);
                }}
              />
              {breedSuggestions.length > 0 && (
                <ul className="breed-dropdown">
                  {breedSuggestions.map((b, idx) => (
                    <li
                      key={idx}
                      onClick={() => {
                        setBreed(b.name);
                        setBreedSuggestions([]);
                      }}
                    >
                      {b.name}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        )}

        {type.toLowerCase() === "other" && (
          <div className="form-group">
            <label>Other Breed *</label>
            <input
              type="text"
              placeholder="e.g. Hamster, Parrot, or Hybrid"
              value={otherBreed}
              onChange={(e) => setOtherBreed(e.target.value)}
              required
            />
          </div>
        )}

        <div className="form-group">
          <label>Birth Date (optional)</label>
          <input
            type="date"
            value={birthDate}
            onChange={(e) => setBirthDate(e.target.value)}
          />
        </div>

        <div className="form-group">
          <label>Weight (kg) (optional)</label>
          <input
            type="number"
            min="0"
            step="0.1"
            placeholder="e.g. 12.5"
            value={weight}
            onChange={(e) => setWeight(e.target.value)}
          />
        </div>

        <div className="form-group">
          <label>Health Issues (comma-separated)</label>
          <input
            type="text"
            placeholder="e.g. allergies, diabetes"
            value={healthIssues}
            onChange={(e) => setHealthIssues(e.target.value)}
          />
        </div>

        <div className="form-group">
          <label>Behavior Issues (comma-separated)</label>
          <input
            type="text"
            placeholder="e.g. aggression, anxiety"
            value={behaviorIssues}
            onChange={(e) => setBehaviorIssues(e.target.value)}
          />
        </div>

        <button type="submit">Create Pet</button>
      </form>
    </div>
  );
}

export default AddPet;
