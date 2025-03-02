import React, { createContext, useContext, useState, useEffect } from "react";
import axios from "axios";
import { API_BASE_URL } from "../config";

// Create AuthContext
export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem("token"));

  // Log in: store token in local storage, set isAuthenticated = true
  const login = (token) => {
    localStorage.setItem("token", token);
    setIsAuthenticated(true);
  };

  // Log out: remove token, set isAuthenticated = false
  const logout = () => {
    localStorage.removeItem("token");
    setIsAuthenticated(false);
  };

  // On mount, verify the stored token by calling /auth/me.
  useEffect(() => {
    async function checkToken() {
      const token = localStorage.getItem("token");
      if (!token) {
        setIsAuthenticated(false);
        return;
      }

      try {
        // This request must succeed for the token to remain valid
        await axios.get(`${API_BASE_URL}/auth/me`);
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
