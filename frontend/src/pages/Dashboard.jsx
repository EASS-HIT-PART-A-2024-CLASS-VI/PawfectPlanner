import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { API_BASE_URL } from "../config";
import "../styles/Dashboard.css";

const Dashboard = () => {
  const [pets, setPets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    axios
      .get(`${API_BASE_URL}/pets`)
      .then((response) => {
        setPets(response.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch pets:", err);
        setError("Failed to load pet data. Please try again later.");
        setLoading(false);
      });
  }, []);

  const handleCreatePet = () => {
    axios
      .post(`${API_BASE_URL}/pets`, {
        name: "New Pet",
        breed: "Unknown",
        weight: 0,
      })
      .then((response) => {
        navigate(`/profile/${response.data.id}`);
      })
      .catch((err) => {
        console.error("Error creating pet:", err);
        setError("Could not create a pet.");
      });
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <div className="dashboard">
      <h2>Your Pets</h2>
      {pets.length === 0 ? (
        <>
          <p>No pets found.</p>
          <button onClick={handleCreatePet}>Create a Pet</button>
        </>
      ) : (
        <ul>
          {pets.map((pet) => (
            <li key={pet.id}>
              <strong>{pet.name}</strong> - {pet.breed}{" "}
              <button onClick={() => navigate(`/profile/${pet.id}`)}>View</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Dashboard;