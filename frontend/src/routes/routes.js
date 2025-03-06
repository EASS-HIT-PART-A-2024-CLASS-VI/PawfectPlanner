// File: frontend/src/routes.js

import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import AboutPage from "./pages/AboutPage";
import Dashboard from "./pages/Dashboard";
import PetProfile from "./pages/PetProfile";
import EditPet from "./pages/EditPet";       // <-- Add your EditPet component
import PawfectGPT from "./pages/PawfectGPT"; // <-- Replaces gemini-service route

function AppRoutes() {
  return (
    <Router>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<HomePage />} />
        <Route path="/about" element={<AboutPage />} />

        {/* Example route for the dashboard (public or protected) */}
        <Route path="/dashboard" element={<Dashboard />} />

        {/* Pet routes */}
        <Route path="/pets/:petId" element={<PetProfile />} />
        <Route path="/edit-pet/:petId" element={<EditPet />} />

        {/* PawfectGPT route (replacing old gemini-service) */}
        <Route path="/pawfectgpt" element={<PawfectGPT />} />

        {/* Fallback */}
        <Route path="*" element={<HomePage />} />
      </Routes>
    </Router>
  );
}

export default AppRoutes;
