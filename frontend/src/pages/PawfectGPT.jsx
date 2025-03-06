// File: frontend/src/pages/PawfectGPT.jsx
import React, { useEffect, useState, useContext } from "react";
import ReactMarkdown from "react-markdown";
import { queryGemini } from "../api/geminiService";
import axiosInstance from "../services/axiosSetup";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import "../styles/PawfectGPT.css";

function PawfectGPT() {
  const { isAuthenticated } = useContext(AuthContext);
  const navigate = useNavigate();

  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState("");
  const [includePetData, setIncludePetData] = useState(false);
  const [petData, setPetData] = useState([]);

  useEffect(() => {
    // If not logged in, redirect
    if (!isAuthenticated) {
      navigate("/login");
    }
  }, [isAuthenticated, navigate]);

  const fetchPetData = async () => {
    try {
      const res = await axiosInstance.get("/pets");
      setPetData(res.data);
    } catch (err) {
      console.error("Error fetching user pets:", err);
    }
  };

  useEffect(() => {
    if (includePetData) {
      fetchPetData();
    }
  }, [includePetData]);

  const handleSend = async () => {
    if (!userInput.trim()) return;

    const newMessages = [...messages, { role: "user", content: userInput }];
    setMessages(newMessages);
    setUserInput("");

    let allPetsSummary = "";
    if (includePetData && petData.length > 0) {
      allPetsSummary = "My pets (weights in kg, birthdates if known):\n";
      petData.forEach((p) => {
        allPetsSummary += `- ${p.name}, type: ${p.type}, breed: ${p.breed}, weight: ${
          p.weight ?? "unknown"
        }, birth_date: ${p.birth_date ?? "unknown"}\n`;
      });
    }

    const prompt = includePetData
      ? `${userInput}\n\n${allPetsSummary}`
      : userInput;

    const aiAnswer = await queryGemini(prompt);
    setMessages([...newMessages, { role: "assistant", content: aiAnswer }]);
  };

  // Determine if we have messages
  const hasMessages = messages.length > 0;

  return (
    <div className="pawfect-gpt-container">
      <h2>PawfectGPT</h2>

      <div className="toggle-wrapper">
        <label>Include all my pet data automatically?</label>
        <input
          type="checkbox"
          checked={includePetData}
          onChange={(e) => setIncludePetData(e.target.checked)}
        />
      </div>

      {/* Chat Window with conditional class */}
      <div className={`chat-window ${hasMessages ? "has-messages" : ""}`}>
        {messages.map((msg, idx) => {
          const isUser = msg.role === "user";
          return (
            <div
              key={idx}
              className={`chat-bubble ${isUser ? "user-bubble" : "assistant-bubble"}`}
            >
              <strong>{isUser ? "You" : "PawfectGPT"}:</strong>{" "}
              <ReactMarkdown>{msg.content}</ReactMarkdown>
            </div>
          );
        })}
      </div>

      <div className="input-section">
        <textarea
          rows={2}
          placeholder="Ask PawfectGPT something..."
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}

export default PawfectGPT;
