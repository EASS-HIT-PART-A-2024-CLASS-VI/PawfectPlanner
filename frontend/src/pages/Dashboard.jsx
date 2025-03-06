// File: frontend/src/pages/Dashboard.jsx
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axiosInstance from "../services/axiosSetup";
import "../styles/Dashboard.css";

const Dashboard = () => {
  const [pets, setPets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchPets() {
      try {
        const res = await axiosInstance.get("/pets");
        setPets(res.data);
      } catch (err) {
        console.error("Failed to fetch pets:", err);
        setError("Could not load pets.");
        setPets([]);
      } finally {
        setLoading(false);
      }
    }
    fetchPets();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <div className="dashboard-container">
      <h2>Your Pets</h2>
      {pets.length === 0 ? (
        <div className="no-pets">
          <p>No pets found. Start by adding a pet!</p>
          <button onClick={() => navigate("/add-pet")}>Add a Pet</button>
        </div>
      ) : (
        <div className="pets-list">
          <button onClick={() => navigate("/add-pet")}>Add a Pet</button>
          <ul>
            {pets.map((pet) => (
              <li key={pet.id}>
                <strong>{pet.name}</strong> - {pet.breed}{" "}
                <button onClick={() => navigate(`/profile/${pet.id}`)}>
                  View
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
