import React, { useEffect, useState } from "react";

const Dashboard = () => {
  const [pets, setPets] = useState([]);

  useEffect(() => {
    fetch("/api/pets")
      .then((res) => res.json())
      .then((data) => setPets(data))
      .catch((err) => console.error("Failed to fetch pets:", err));
  }, []);

  return (
    <div>
      <h2>Your Pets</h2>
      {pets.length > 0 ? (
        pets.map((pet) => (
          <div key={pet.id} className="pet-card">
            <strong>{pet.name}</strong> ({pet.type}) - {pet.breed}
            <p>Age: {pet.age ? pet.age + " years" : "Unknown"}</p>
            <p>Weight: {pet.weight ? pet.weight + " kg" : "Unknown"}</p>
          </div>
        ))
      ) : (
        <p>No pets found.</p>
      )}
    </div>
  );
};

export default Dashboard;
