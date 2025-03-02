// src/pages/PetProfile.jsx
import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import { API_BASE_URL } from "../config";
import { generatePetPDF } from "../utils/generatePDF";
import "../styles/PetProfile.css";

import { queryGeminiStrictJson } from "../api/geminiService";

const PetProfile = () => {
  const { petId } = useParams();
  const navigate = useNavigate();
  const [pet, setPet] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState({});

  useEffect(() => {
    // If no param is given, redirect to /dashboard
    if (!petId || petId === "undefined") {
      navigate("/dashboard");
      return;
    }
  
    setLoading(true);
    axios
      .get(`${API_BASE_URL}/pets/${petId}`)
      .then((response) => {
        setPet(response.data);
        setFormData(response.data);
      })
      .catch((err) => {
        console.error("Error fetching pet:", err);
        setError("Failed to load pet details.");
      })
      .finally(() => setLoading(false));
  }, [petId]);
  

  // Save updated changes
  const handleEdit = () => {
    axios
      .put(`${API_BASE_URL}/pets/${petId}`, formData)
      .then((response) => {
        setPet(response.data);
        setEditMode(false);
      })
      .catch((err) => {
        console.error("Error updating pet:", err);
      });
  };

  // Delete pet
  const handleDelete = () => {
    axios
      .delete(`${API_BASE_URL}/pets/${petId}`)
      .then(() => {
        navigate("/dashboard");
      })
      .catch((err) => {
        console.error("Error deleting pet:", err);
      });
  };

  // NEW: Call Gemini for breed data if breed == "other"
  const handleFetchFromGemini = async () => {
    const prompt = `Provide approximate 'weight', 'life_span', 'temperament', and 'health_issues' for a ${formData.other_breed} (pet type: ${formData.type}). Return valid JSON only.`;
    const result = await queryGeminiStrictJson(prompt);
    if (result.success) {
      const { weight, life_span, temperament, health_issues } = result.data;
      // We'll just store them in the front-end formData
      // We can't update the backend's Pet table because there's no columns for them,
      // but you can show them in the UI or store them in new formData fields
      alert(`Gemini gave us:
Weight: ${weight}
Life Span: ${life_span}
Temperament: ${temperament}
Health Issues: ${health_issues}
`);
    } else {
      alert("Gemini gave invalid JSON twice. Please fill data manually.");
    }
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <div className="pet-profile">
      <h2>{pet.name}'s Profile</h2>
      <p><strong>Breed:</strong> {pet.breed}</p>

      {pet.breed_info && (
        <div className="breed-info">
          <p><strong>Life Expectancy:</strong> {pet.breed_info.life_expectancy || "Unknown"}</p>
          <p><strong>Temperament:</strong> {pet.breed_info.temperament || "Unknown"}</p>
          <p><strong>Known Health Issues:</strong> {pet.breed_info.health_issues || "None"}</p>
          <p>
            <strong>Weight:</strong> {pet.weight} kg
            {pet.breed_info.average_weight && (
              <span> (Recommended: {pet.breed_info.average_weight} kg)</span>
            )}
          </p>
          {pet.weight &&
            pet.breed_info.average_weight &&
            (pet.weight > parseFloat(pet.breed_info.average_weight) * 1.2 ||
              pet.weight < parseFloat(pet.breed_info.average_weight) * 0.8) && (
              <p className="warning">⚠️ {pet.name} is outside the recommended weight range!</p>
            )}
        </div>
      )}

      {editMode ? (
        <div className="edit-form">
          <label>Pet Name:</label>
          <input
            type="text"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          />
          
          <label>Weight (kg):</label>
          <input
            type="number"
            value={formData.weight || ""}
            onChange={(e) => setFormData({ ...formData, weight: e.target.value })}
          />

          <button onClick={handleEdit}>Save</button>
          <button onClick={() => setEditMode(false)} className="cancel-button">Cancel</button>

          {/* If the breed is 'other', show a "Fetch from Gemini" button */}
          {formData.breed === "other" && (
            <button type="button" onClick={handleFetchFromGemini}>
              Fetch Data from Gemini
            </button>
          )}
        </div>
      ) : (
        <button onClick={() => setEditMode(true)}>Edit</button>
      )}

      <button onClick={handleDelete} className="delete-button">Delete Pet</button>
      <button onClick={() => generatePetPDF(pet)} className="download-pdf">Download Pet Profile</button>
    </div>
  );
};

export default PetProfile;
