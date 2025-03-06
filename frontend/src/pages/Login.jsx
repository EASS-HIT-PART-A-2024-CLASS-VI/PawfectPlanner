// File: frontend/src/pages/Login.jsx
import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../services/authService";
import { AuthContext } from "../context/AuthContext";
import "../styles/global.css";  // main global
import "../styles/Auth.css";    // for narrower fields

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const { login: contextLogin } = useContext(AuthContext);

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await login(email, password);
      if (response && response.access_token) {
        contextLogin(response.access_token); // store token in context
        alert("Login successful!");
        navigate("/dashboard");
      } else {
        alert("Login failed: missing token in response");
      }
    } catch (error) {
      console.error("Login error:", error);
      alert("Invalid credentials");
    }
  };

  return (
    <div className="auth-container">
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;
