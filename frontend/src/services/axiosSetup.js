// File: frontend/src/services/axiosSetup.js
import axios from "axios";
import { API_BASE_URL } from "../config";

// 1) Main backend instance => baseURL="/api"
const axiosInstance = axios.create({
  baseURL: API_BASE_URL, // e.g. "/api"
});

axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 2) Gemini instance => baseURL="/gemini"
export const geminiAxios = axios.create({
  baseURL: "/gemini"
});

geminiAxios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default axiosInstance;
