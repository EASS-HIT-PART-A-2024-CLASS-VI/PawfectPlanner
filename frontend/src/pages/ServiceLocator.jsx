// File: frontend/src/pages/ServiceLocator.jsx
import React from "react";
import "../styles/ServiceLocator.css";

function ServiceLocator() {
  const openVetSearch = () => {
    window.open("https://www.google.com/maps/search/veterinary+clinic", "_blank");
  };
  const openGroomingSearch = () => {
    window.open("https://www.google.com/maps/search/pet+grooming", "_blank");
  };
  const openStoreSearch = () => {
    window.open("https://www.google.com/maps/search/pet+store", "_blank");
  };

  return (
    <div className="service-container">
      <h2>Find Pet Services</h2>
      <p>Select a service to search on Google Maps:</p>
      <button onClick={openVetSearch}>Vet Services</button>
      <button onClick={openGroomingSearch}>Pet Grooming</button>
      <button onClick={openStoreSearch}>Pet Stores</button>
    </div>
  );
}

export default ServiceLocator;
