# File: backend/gemini-service/app.py

import os
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from google import genai  # The official Google library
from pydantic import BaseModel

app = FastAPI()

# Enable CORS so the front end at http://localhost:3000 can call this microservice at http://localhost:5000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] if you want to restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set. Please add it to your .env file.")

# Create the Gemini client once at startup
client = genai.Client(api_key=GEMINI_API_KEY)

# Example model name: "gemini-2.0-flash" or "gemini-1.0"
MODEL_NAME = "gemini-2.0-flash"

# A system prompt that restricts queries to pet care topics
SYSTEM_PROMPT = """
You are PawfectPlanner GPT, an AI specialized in pet care, behavior, and health.
You only answer pet-related questions. If the user asks about anything else,
politely decline or redirect them.
"""

class GeminiRequest(BaseModel):
    """
    Body for the /gemini/query endpoint.
    """
    prompt: str
    pet: dict = {}
    forceJSON: bool = False

@app.post("/gemini/query")
async def query_gemini(data: GeminiRequest):
    """
    A single endpoint to query the Gemini LLM via the google-genai library.

    Request body:
    {
      "prompt": "...",
      "pet": {... optional fields ...},
      "forceJSON": boolean
    }
    """

    user_prompt = data.prompt
    pet_data = data.pet
    force_json = data.forceJSON

    if not user_prompt.strip():
        raise HTTPException(status_code=400, detail="Missing prompt.")

    # 1) Start with system instructions to keep answers pet-related
    final_prompt = SYSTEM_PROMPT.strip()

    # 2) Add user prompt
    final_prompt += f"\n\nUser's question: {user_prompt}"

    # 3) If there's pet data, add it
    if pet_data:
        final_prompt += "\n\nAdditional pet data:\n"
        for k, v in pet_data.items():
            final_prompt += f"- {k}: {v}\n"

    # 4) If we want strictly JSON, instruct the model
    if force_json:
        final_prompt += """
        
Respond ONLY in valid JSON with keys:
{ "weight": "...", "life_span": "...", "temperament": "...", "health_issues": "..." }
No extra text, no explanations.
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=final_prompt
        )
        # This returns a "Result" object; response.text is the final string
        gemini_answer = response.text
        return {"answer": gemini_answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling Gemini: {e}")
