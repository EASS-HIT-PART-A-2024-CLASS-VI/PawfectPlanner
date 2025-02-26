import React from 'react';
import "../styles/Home.css";

const Home = () => {
  return (
    <div className="home-container">
      <h1>Welcome to Pawfect Planner</h1>
      <p>Track and manage your pet’s health and schedule.</p>
      <img src="/EntryBackground.png" alt="Happy Pet" className="home-image" />
    </div>
  );
};

export default Home;
