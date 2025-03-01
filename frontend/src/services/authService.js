import axios from "axios";
import { API_BASE_URL } from "../config"; // Ensure API URL is always correct

const API_URL = `${API_BASE_URL}/auth`;

export const signup = async (email, password) => {
  try {
    const response = await axios.post(`${API_URL}/register`, { email, password });
    return response.data;
  } catch (error) {
    console.error("Signup failed:", error.response?.data?.detail || error.message);
    throw error;
  }
};

export const login = async (email, password) => {
  try {
    const response = await axios.post(`${API_URL}/login`, { email, password });
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

// Attach token to every request
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);
