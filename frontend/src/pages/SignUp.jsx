// File: frontend/src/pages/SignUp.jsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { signup } from "../services/authService";
import "../styles/global.css";
import "../styles/Auth.css";

const Signup = () => {
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      await signup(formData.email, formData.password);
      alert("Signup successful!");
      navigate("/dashboard");
    } catch (err) {
      console.error("Signup error:", err.response || err);
      if (err.response) {
        const status = err.response.status;
        if (status === 400) {
          setError("Email already registered. Try another.");
        } else if (status === 422) {
          setError("Invalid email format or missing password.");
        } else if (status === 500) {
          setError("Server error. Try again later.");
        } else {
          setError(err.response.data.detail || "Signup failed.");
        }
      } else {
        setError("Network error. Check your connection.");
      }
    }
  };

  return (
    <div className="auth-container">
      <h2>Sign Up</h2>
      <form onSubmit={handleSignup}>
        <input
          type="email"
          placeholder="Email"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={formData.password}
          onChange={(e) => setFormData({ ...formData, password: e.target.value })}
          required
        />
        <button type="submit">Sign Up</button>
      </form>
      {error && <p className="error">{error}</p>}
    </div>
  );
};

export default Signup;
