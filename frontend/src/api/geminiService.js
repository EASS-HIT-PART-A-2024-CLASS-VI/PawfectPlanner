// File: frontend/src/api/geminiService.js
import axios from "axios";
import { API_BASE_URL } from "../config";

/**
 * queryGemini: Basic usage to get a free-form answer
 */
export async function queryGemini(prompt, pet = {}) {
  try {
    const response = await axios.post(`${API_BASE_URL}/gemini/query`, {
      prompt,
      pet,
      forceJSON: false
    });
    return response.data.answer || "No response from AI.";
  } catch (error) {
    console.error("Error fetching Gemini AI response:", error);
    return "Could not fetch AI advice.";
  }
}

/**
 * queryGeminiStrictJson: tries to get strict JSON with the specified keys:
 * { weight, life_span, temperament, health_issues }
 * We'll do up to 2 attempts if parsing fails.
 */
export async function queryGeminiStrictJson(prompt, pet = {}) {
  // 1st attempt
  const initial = await attemptJson(prompt, pet);
  if (initial.success) {
    return { success: true, data: initial.data };
  }
  // If that fails, re-ask the model
  console.log("Gemini did not return valid JSON. Trying second attempt...");
  const second = await attemptJson("You did not follow JSON format. Return strictly valid JSON only:\n" + prompt, pet);
  if (second.success) {
    return { success: true, data: second.data };
  }
  // If that fails again, user must fill manually
  return { success: false, error: "Gemini returned invalid JSON twice." };
}

async function attemptJson(prompt, pet) {
  try {
    const response = await axios.post(`${API_BASE_URL}/gemini/query`, {
      prompt,
      pet,
      forceJSON: true
    });
    const text = response.data.answer || "";
    // Attempt to parse
    const parsed = JSON.parse(text);
    // If it parsed, we assume it matches the structure
    return { success: true, data: parsed };
  } catch (err) {
    console.warn("Attempt to parse Gemini JSON failed:", err);
    return { success: false, error: err };
  }
}
