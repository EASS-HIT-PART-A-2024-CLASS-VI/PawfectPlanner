// File: frontend/src/services/authService.js
import axiosInstance from "../services/axiosSetup";

export const signup = async (email, password) => {
  try {
    const response = await axiosInstance.post("/auth/register", { email, password });
    return response.data;
  } catch (error) {
    console.error("Signup failed:", error.response?.data?.detail || error.message);
    throw error;
  }
};

export const login = async (email, password) => {
  try {
    const response = await axiosInstance.post("/auth/login", { email, password });
    localStorage.setItem("token", response.data.access_token);
    return response.data;
  } catch (error) {
    console.error("Login failed:", error.response?.data?.detail || error.message);
    throw error;
  }
};

export const logout = () => localStorage.removeItem("token");

export const isAuthenticated = () => {
  try {
    const token = localStorage.getItem("token");
    if (!token) return false;

    const decoded = JSON.parse(atob(token.split(".")[1]));
    return decoded.exp * 1000 > Date.now();
  } catch (error) {
    console.warn("Invalid token detected, logging out...");
    logout();
    return false;
  }
};
