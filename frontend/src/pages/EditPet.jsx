import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate, useParams } from "react-router-dom";

const EditPet = () => {
  const { id } = useParams();
  const [pet, setPet] = useState({ name: "", breed: "", weight: "" });
  const navigate = useNavigate();

  useEffect(() => {
    axios.get(`/api/pets/${id}`).then((res) => setPet(res.data));
  }, [id]);

  const handleChange = (e) => setPet({ ...pet, [e.target.name]: e.target.value });

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.put(`/api/pets/${id}`, pet)
      .then(() => navigate(`/profile/${id}`))
      .catch((err) => console.error("Error updating pet:", err));
  };

  return (
    <div>
      <h2>Edit Pet</h2>
      <form onSubmit={handleSubmit}>
        <label>Name:</label>
        <input type="text" name="name" value={pet.name} onChange={handleChange} />

        <label>Breed:</label>
        <input type="text" name="breed" value={pet.breed} onChange={handleChange} />

        <label>Weight:</label>
        <input type="number" name="weight" value={pet.weight} onChange={handleChange} />

        <button type="submit">Save Changes</button>
      </form>
    </div>
  );
};

export default EditPet;
