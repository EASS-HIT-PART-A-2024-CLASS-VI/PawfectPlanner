// File: frontend/src/pages/EditPet.jsx
import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axiosInstance from "../services/axiosSetup";
import "../styles/EditPet.css";

function EditPet() {
  const { petId } = useParams();
  const navigate = useNavigate();
  const [pet, setPet] = useState({
    name: "",
    type: "dog",
    breed: "",
    other_breed: "",
    weight: "",
    health_issues: "",
    behavior_issues: ""
  });

  useEffect(() => {
    axiosInstance
      .get(`/pets/${petId}`)
      .then((res) => {
        setPet(res.data);
      })
      .catch((err) => console.error("Error loading pet data:", err));
  }, [petId]);

  const handleChange = (e) => {
    setPet({ ...pet, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Convert comma strings to arrays if needed
    let updatedPet = { ...pet };
    if (typeof pet.health_issues === "string") {
      updatedPet.health_issues = pet.health_issues
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean);
    }
    if (typeof pet.behavior_issues === "string") {
      updatedPet.behavior_issues = pet.behavior_issues
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean);
    }

    axiosInstance
      .put(`/pets/${petId}`, updatedPet)
      .then(() => {
        alert("Pet updated successfully!");
        navigate(`/profile/${petId}`);
      })
      .catch((err) => {
        console.error("Error updating pet:", err);
        alert("Could not update pet.");
      });
  };

  return (
    <div className="edit-pet-container">
      <h2>Edit Pet Profile</h2>
      <form onSubmit={handleSubmit}>
        <label>Name:</label>
        <input
          type="text"
          name="name"
          value={pet.name || ""}
          onChange={handleChange}
        />

        {/* Instead of letting user change type/breed, show them read-only */}
        <label>Type:</label>
        <input
          type="text"
          name="type"
          value={pet.type || ""}
          disabled
        />

        <label>Breed:</label>
        <input
          type="text"
          name="breed"
          value={pet.breed || ""}
          disabled
        />

        {/* If pet.type === "other", we might still show the other_breed, but read-only */}
        {pet.type === "other" && (
          <>
            <label>Other Breed:</label>
            <input
              type="text"
              name="other_breed"
              value={pet.other_breed || ""}
              disabled
            />
          </>
        )}

        <label>Weight (kg):</label>
        <input
          type="number"
          name="weight"
          min="0"
          step="0.1"
          value={pet.weight || ""}
          onChange={handleChange}
        />

        <label>Health Issues (comma-separated):</label>
        <input
          type="text"
          name="health_issues"
          placeholder="e.g. allergies, diabetes"
          value={
            Array.isArray(pet.health_issues)
              ? pet.health_issues.join(", ")
              : pet.health_issues || ""
          }
          onChange={handleChange}
        />

        <label>Behavior Issues (comma-separated):</label>
        <input
          type="text"
          name="behavior_issues"
          placeholder="e.g. aggression, anxiety"
          value={
            Array.isArray(pet.behavior_issues)
              ? pet.behavior_issues.join(", ")
              : pet.behavior_issues || ""
          }
          onChange={handleChange}
        />

        <button type="submit">Save Changes</button>
      </form>
    </div>
  );
}

export default EditPet;
