import axios from "axios";
import { API_BASE_URL } from "../config";

export const getGeminiAdvice = async (prompt) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/gemini/advice`, { prompt });
    return response.data.advice;
  } catch (error) {
    console.error("Error fetching Gemini AI response:", error);
    return "Could not fetch AI advice.";
  }
};