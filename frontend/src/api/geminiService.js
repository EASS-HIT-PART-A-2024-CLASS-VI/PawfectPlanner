// File: frontend/src/api/geminiService.js
import { geminiAxios } from "../services/axiosSetup.js";

// We'll hit "/gemini/query" instead of a hard-coded localhost URL
const GEMINI_ENDPOINT = "/query";

/**
 * queryGemini: Basic usage to get a free-form answer
 */
export async function queryGemini(prompt, pet = {}) {
  try {
    const response = await geminiAxios.post(GEMINI_ENDPOINT, {
      prompt,
      pet,
      forceJSON: false,
    });
    return response.data.answer || "No response from AI.";
  } catch (error) {
    console.error("Error fetching Gemini AI response:", error);
    // You could throw an Error here or return a more descriptive message
    return "Could not fetch AI advice.";
  }
}

/**
 * queryGeminiStrictJson: tries to get strict JSON with the specified keys:
 * { weight, life_span, temperament, health_issues }
 */
export async function queryGeminiStrictJson(prompt, pet = {}) {
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
    const response = await geminiAxios.post(GEMINI_ENDPOINT, {
      prompt,
      pet,
      forceJSON: true,
    });
    const text = response.data.answer || "";
    const parsed = JSON.parse(text);
    return { success: true, data: parsed };
  } catch (err) {
    console.warn("Attempt to parse Gemini JSON failed:", err);
    return { success: false, error: err };
  }
}
