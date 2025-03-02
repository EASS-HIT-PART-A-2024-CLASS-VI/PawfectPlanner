import React, { useState, useEffect } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import PetProfile from "./pages/PetProfile";
import Reminders from "./pages/Reminders";
import Treatments from "./pages/Treatments";
import VetLocator from "./pages/VetLocator";
import Login from "./pages/Login";
import SignUp from "./pages/SignUp";
import Dashboard from "./pages/Dashboard";
import GeminiService from "./pages/GeminiService";  // <--- If you want this route
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
          <Route path="/" element={<Home />} />
          
          {/* Public route for GeminiService if you want anyone to access it */}
          <Route path="/gemini-service" element={<GeminiService />} />

          <Route
            path="/profile"
            element={
              <PrivateRoute>
                <PetProfile />
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
            path="/vet-locator"
            element={
              <PrivateRoute>
                <VetLocator />
              </PrivateRoute>
            }
          />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            }
          />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </AuthProvider>
  );
}

export default App;
