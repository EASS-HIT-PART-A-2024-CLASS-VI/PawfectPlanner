// File: frontend/src/pages/GeminiService.jsx

import React, { useState } from "react";
import { queryGemini } from "../api/geminiService";
import "../styles/GeminiService.css";

const GeminiService = () => {
  // We store a conversation array of messages: [{role: "user"|"assistant", content: string}]
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState("");
  const [petType, setPetType] = useState("dog");
  const [breed, setBreed] = useState("");
  const [weight, setWeight] = useState("");

  const handleSend = async () => {
    if (!userInput.trim()) return;

    // 1) Add user's message to the conversation
    const newMessages = [...messages, { role: "user", content: userInput }];
    setMessages(newMessages);
    setUserInput("");

    // 2) Optional: pass pet data
    const petData = {
      type: petType,
      breed: breed,
      weight: weight ? parseFloat(weight) : undefined
    };

    // 3) Query Gemini
    const aiAnswer = await queryGemini(userInput, petData);

    // 4) Add AI's response to conversation
    setMessages([...newMessages, { role: "assistant", content: aiAnswer }]);
  };

  return (
    <div className="gemini-chat">
      <h2>Gemini AI Chat</h2>

      <div className="pet-data-section">
        <label>Pet Type: </label>
        <input
          type="text"
          value={petType}
          onChange={(e) => setPetType(e.target.value)}
        />
        <label>Breed: </label>
        <input
          type="text"
          value={breed}
          onChange={(e) => setBreed(e.target.value)}
        />
        <label>Weight (kg): </label>
        <input
          type="number"
          value={weight}
          onChange={(e) => setWeight(e.target.value)}
        />
      </div>

      <div className="chat-window">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={msg.role === "user" ? "user-message" : "assistant-message"}
          >
            <strong>{msg.role === "user" ? "You" : "Gemini"}:</strong>{" "}
            {msg.content}
          </div>
        ))}
      </div>

      <div className="input-section">
        <textarea
          rows={2}
          placeholder="Ask Gemini something about pet care..."
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
};

export default GeminiService;
