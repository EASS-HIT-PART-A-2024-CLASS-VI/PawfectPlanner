import axios from 'axios';

const API_URL = '/api/auth'; // Corrected endpoint

export const signup = (email, password) => {
  return axios.post(`${API_URL}/register`, { email, password });
};

export const login = (email, password) => {
  return axios.post(`${API_URL}/login`, { email, password });
};

export const logout = () => {
  localStorage.removeItem('token');
};

export const isAuthenticated = () => {
  return !!localStorage.getItem('token');
};