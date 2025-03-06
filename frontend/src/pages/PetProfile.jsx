// File: frontend/src/pages/PetProfile.jsx

import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axiosInstance from "../services/axiosSetup";
import { generatePetPDF } from "../utils/generatePDF";
import { differenceInYears } from "date-fns";
import "../styles/PetProfile.css";

function PetProfile() {
  const { petId } = useParams();
  const navigate = useNavigate();
  const [pet, setPet] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchPet() {
      try {
        const res = await axiosInstance.get(`/pets/${petId}`);
        setPet(res.data);
      } catch (err) {
        console.error("Failed to load pet:", err);
        setError("Could not load pet details.");
      } finally {
        setLoading(false);
      }
    }
    fetchPet();
  }, [petId]);

  if (loading) return <p>Loading pet data...</p>;
  if (error) return <p className="error">{error}</p>;
  if (!pet) return <p>No pet found with ID {petId}</p>;

  /**
   * Checks if pet.weight is outside the recommended average_weight_range
   * (if provided by the breed API). Returns a warning string if so.
   */
  const getWeightWarning = () => {
    // If no average range or no weight, skip
    if (!pet.average_weight_range || pet.average_weight_range === "Unknown" || !pet.weight) {
      return "";
    }
  
    // Example: "9 - 13" or "25 - 34" or sometimes just "13"
    let rangeStr = pet.average_weight_range.trim().replace(/\s*kg\s*/gi, "");
    const parts = rangeStr.split("-").map((p) => p.trim());
  
    if (parts.length === 2) {
      // Normal dash‐based range
      const minVal = parseFloat(parts[0]);
      const maxVal = parseFloat(parts[1]);
      if (!isNaN(minVal) && !isNaN(maxVal)) {
        const lower = minVal * 0.8; // 20% below min
        const upper = maxVal * 1.2; // 20% above max
        if (pet.weight < lower || pet.weight > upper) {
          return "Weight is far from the breed's average!";
        }
      }
    } else if (parts.length === 1) {
      // Single numeric value: treat it as val ± 20%
      const val = parseFloat(parts[0]);
      if (!isNaN(val)) {
        const lower = val * 0.8;
        const upper = val * 1.2;
        if (pet.weight < lower || pet.weight > upper) {
          return "Weight is far from the breed's average!";
        }
      }
    }
    return "";
  };

  // Compute approximate age if birth_date is available
  let ageString = "";
  if (pet.birth_date) {
    try {
      const birth = new Date(pet.birth_date);
      const ageYears = differenceInYears(new Date(), birth);
      ageString = ` (Age ~ ${ageYears})`;
    } catch (error) {
      // fallback
    }
  }

  /**
   * Delete the pet by ID, then navigate back to dashboard.
   */
  const handleDelete = async () => {
    try {
      await axiosInstance.delete(`/pets/${petId}`);
      alert("Pet deleted successfully!");
      navigate("/dashboard");
    } catch (error) {
      console.error("Error deleting pet:", error);
      alert("Could not delete pet.");
    }
  };

  const weightWarning = getWeightWarning();

  return (
    <div className="pet-profile">
      <h2>{pet.name}'s Profile</h2>

      <p><strong>Type:</strong> {pet.type}</p>
      <p><strong>Breed:</strong> {pet.breed}</p>
      {pet.breed === "other" && pet.other_breed && (
        <p><strong>Other Breed:</strong> {pet.other_breed}</p>
      )}

      {/* Birth Date + approximate age */}
      {pet.birth_date && (
        <p>
          <strong>Birth Date:</strong>{" "}
          {new Date(pet.birth_date).toLocaleDateString()}
          {ageString}
        </p>
      )}

      {/* Weight */}
      <p>
        <strong>Weight:</strong>{" "}
        {pet.weight ? `${pet.weight} kg` : "Not defined"}
      </p>

      {/* Additional breed data */}
      {pet.average_weight_range && (
        <p>
          <strong>Recommended Range:</strong> {pet.average_weight_range} kg
        </p>
      )}
      {pet.life_expectancy && (
        <p>
          <strong>Life Expectancy:</strong> {pet.life_expectancy}
        </p>
      )}
      {pet.temperament && (
        <p>
          <strong>Temperament:</strong> {pet.temperament}
        </p>
      )}
      {pet.bred_for && (
        <p>
          <strong>Bred For:</strong> {pet.bred_for}
        </p>
      )}
      {pet.breed_group && (
        <p>
          <strong>Breed Group:</strong> {pet.breed_group}
        </p>
      )}

      {/* Health & Behavior */}
      {pet.health_issues && pet.health_issues.length > 0 && (
        <p>
          <strong>Health Issues:</strong>{" "}
          {pet.health_issues.join(", ")}
        </p>
      )}
      {pet.behavior_issues && pet.behavior_issues.length > 0 && (
        <p>
          <strong>Behavior Issues:</strong>{" "}
          {pet.behavior_issues.join(", ")}
        </p>
      )}

      {/* Weight warning if out-of-range */}
      {weightWarning && (
        <p className="warning" style={{ color: "red", fontWeight: "bold" }}>
          {weightWarning}
        </p>
      )}

      <div className="pet-actions" style={{ marginTop: "1rem" }}>
        <button
          style={{ marginRight: "1rem" }}
          onClick={() => generatePetPDF(pet)}
        >
          Download Pet Profile PDF
        </button>
        <button
          style={{ marginRight: "1rem" }}
          onClick={() => navigate(`/edit-pet/${pet.id}`)}
        >
          Edit Pet
        </button>
        <button onClick={handleDelete}>Delete Pet</button>
      </div>
    </div>
  );
}

export default PetProfile;
