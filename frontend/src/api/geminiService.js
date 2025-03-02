// File: frontend/src/api/geminiService.js

import axios from "axios";

/**
 * We skip API_BASE_URL for now, calling the Gemini container directly.
 * If you prefer an Nginx reverse proxy, you can set that up. 
 * But simplest is direct to http://localhost:5000
 */

const GEMINI_URL = "http://localhost:5000/gemini/query";

/**
 * queryGemini: Basic usage to get a free-form answer
 */
export async function queryGemini(prompt, pet = {}) {
  try {
    const response = await axios.post(GEMINI_URL, {
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

  console.log("Gemini did not return valid JSON. Trying second attempt...");
  const second = await attemptJson(
    "You did not follow JSON format. Return strictly valid JSON only:\n" + prompt,
    pet
  );
  if (second.success) {
    return { success: true, data: second.data };
  }

  // If that fails again, user must fill manually
  return { success: false, error: "Gemini returned invalid JSON twice." };
}

async function attemptJson(prompt, pet) {
  try {
    const response = await axios.post(GEMINI_URL, {
      prompt,
      pet,
      forceJSON: true
    });
    const text = response.data.answer || "";
    const parsed = JSON.parse(text);
    return { success: true, data: parsed };
  } catch (err) {
    console.warn("Attempt to parse Gemini JSON failed:", err);
    return { success: false, error: err };
  }
}
