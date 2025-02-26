import React, { useState } from "react";
import "../styles/GeminiService.css";

const GeminiService = () => {
  const [response, setResponse] = useState("");

  const getAIResponse = async (query) => {
    try {
      const res = await fetch("/api/gemini", {
        method: "POST",
        body: JSON.stringify({ query }),
        headers: { "Content-Type": "application/json" },
      });
      const data = await res.json();
      setResponse(data.answer);
    } catch (error) {
      console.error("Failed to fetch AI response:", error);
    }
  };

  return (
    <div className="gemini-container">
      <h2>Advice from Gemini AI</h2>
      <button onClick={() => getAIResponse("Tell me about dog care")}>Ask Gemini</button>
      <p className="gemini-response">{response}</p>
    </div>
  );
};

export default GeminiService;
