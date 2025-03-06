// File: frontend/src/context/AuthContext.jsx

import React, { createContext, useContext, useState, useEffect } from "react";
import axiosInstance from "../services/axiosSetup.js"; 

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem("token"));

  const login = (token) => {
    localStorage.setItem("token", token);
    setIsAuthenticated(true);
  };

  const logout = () => {
    localStorage.removeItem("token");
    setIsAuthenticated(false);
  };

  useEffect(() => {
    async function checkToken() {
      const token = localStorage.getItem("token");
      if (!token) {
        setIsAuthenticated(false);
        return;
      }

      try {
        // Use axiosInstance so the Authorization header is included
        await axiosInstance.get(`/auth/me`);
        setIsAuthenticated(true);
      } catch (err) {
        console.warn("Token invalid or expired, forcing logout");
        logout();
      }
    }

    checkToken();
  }, []);

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
