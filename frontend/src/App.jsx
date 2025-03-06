// File: frontend/src/App.jsx
import React, { useState, useEffect } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import PetProfile from "./pages/PetProfile";
import AddPet from "./pages/AddPet";
import EditPet from "./pages/EditPet";
import Reminders from "./pages/Reminders";
import Treatments from "./pages/Treatments";
import ServiceLocator from "./pages/ServiceLocator";
import Login from "./pages/Login";
import SignUp from "./pages/SignUp";
import Dashboard from "./pages/Dashboard";
import PawfectGPT from "./pages/PawfectGPT";
import { ScaleLoader } from "react-spinners";

function PrivateRoute({ children }) {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" />;
}

function App() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => setLoading(false), 1000);
  }, []);

  if (loading) {
    return (
      <div className="loading-container">
        <ScaleLoader />
      </div>
    );
  }

  return (
    <AuthProvider>
      <Navbar />
      <div className="container">
        <Routes>
          {/* Public Home */}
          <Route path="/" element={<Home />} />

          {/* Public PawfectGPT route */}
          <Route path="/pawfectgpt" element={<PawfectGPT />} />

          {/* Protected Routes */}
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            }
          />
          <Route
            path="/add-pet"
            element={
              <PrivateRoute>
                <AddPet />
              </PrivateRoute>
            }
          />
          <Route
            path="/profile/:petId"
            element={
              <PrivateRoute>
                <PetProfile />
              </PrivateRoute>
            }
          />
          <Route
            path="/edit-pet/:petId"
            element={
              <PrivateRoute>
                <EditPet />
              </PrivateRoute>
            }
          />
          <Route
            path="/reminders"
            element={
              <PrivateRoute>
                <Reminders />
              </PrivateRoute>
            }
          />
          <Route
            path="/treatments"
            element={
              <PrivateRoute>
                <Treatments />
              </PrivateRoute>
            }
          />
          <Route
            path="/services"
            element={
              <PrivateRoute>
                <ServiceLocator />
              </PrivateRoute>
            }
          />

          {/* Public Auth */}
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </AuthProvider>
  );
}

export default App;
