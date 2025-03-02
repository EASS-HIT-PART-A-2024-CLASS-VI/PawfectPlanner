// File: src/pages/Dashboard.jsx

import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { API_BASE_URL } from "../config";
import "../styles/Dashboard.css";

const Dashboard = () => {
  const [pets, setPets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [userId, setUserId] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchUser() {
      try {
        // Attempt to get the current user's info (including ID) from /auth/me
        const res = await axios.get(`${API_BASE_URL}/auth/me`);
        return res.data; // e.g. { email: "user@demo.com" }
      } catch (err) {
        console.error("Failed to fetch user info:", err);
        return null;
      }
    }

    async function init() {
      // 1) Fetch user info
      const userData = await fetchUser();
      if (userData && userData.email) {
        // If your /auth/me endpoint also returns an "id", store it:
        // e.g. userData = { email: "user@demo.com", id: 123 }
        if (userData.id) {
          setUserId(userData.id);
        }
      } else {
        console.warn("No user ID found. Creating a pet may fail if schema requires owner_id.");
      }

      // 2) Fetch existing pets
      try {
        const petsRes = await axios.get(`${API_BASE_URL}/pets`);
        setPets(petsRes.data);
      } catch (err) {
        console.error("Failed to fetch pets:", err);
        setError("Failed to load pet data. Please try again later.");
      } finally {
        setLoading(false);
      }
    }

    init();
  }, []);

  // Called when user clicks "Create a Pet"
  const handleCreatePet = async () => {
    try {
      if (!userId) {
        alert("No user ID found. Please ensure you're logged in.");
        return;
      }

      // Make POST request with the required fields
      const createRes = await axios.post(`${API_BASE_URL}/pets`, {
        name: "New Pet",
        breed: "Unknown",
        weight: 0,
        owner_id: userId
      });

      // On success, show alert
      alert("Pet created!");

      // Navigate to the newly created pet’s profile page
      navigate(`/profile/${createRes.data.id}`);
    } catch (err) {
      console.error("Error creating pet:", err);
      setError("Could not create a pet.");
    }
  };

  // While loading data
  if (loading) return <p>Loading...</p>;
  // If an error occurred
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
