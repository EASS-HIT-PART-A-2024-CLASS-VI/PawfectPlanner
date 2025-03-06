# File: backend/gemini_service/geminiRun.py

import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Body
from google import genai
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.env"))
load_dotenv(dotenv_path=dotenv_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    logger.error("❌ GEMINI_API_KEY is missing! Set it in the .env file.")

try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    logger.error(f"❌ Failed to initialize Gemini client: {e}")
    client = None

app = FastAPI()

MODEL_NAME = "gemini-2.0-flash"

SYSTEM_PROMPT = """
You are PawfectPlanner GPT, an AI specialized in pet care, pet behavior, and pet health.
You only answer pet-related questions. If the user asks about anything else,
politely decline or redirect them.
"""

class GeminiRequest(BaseModel):
    prompt: str
    pet: dict = {}
    forceJSON: bool = False

# Change to "/query" so external calls to "/gemini/query" become "/query" inside the container
@app.post("/query")
async def query_gemini(data: GeminiRequest):
    user_prompt = data.prompt.strip()
    if not user_prompt:
        raise HTTPException(status_code=400, detail="Missing prompt.")

    final_prompt = f"{SYSTEM_PROMPT.strip()}\n\nUser's question: {user_prompt}"
    if data.pet:
        final_prompt += "\n\nAdditional pet data:\n" + "\n".join(f"- {k}: {v}" for k, v in data.pet.items())

    if data.forceJSON:
        final_prompt += """
        Respond ONLY in valid JSON with keys:
        { "weight": "...", "life_span": "...", "temperament": "...", "health_issues": "..." }
        No extra text, no explanations.
        """

    if client is None:
        raise HTTPException(status_code=500, detail="Gemini service is unavailable.")

    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=final_prompt)
        return {"answer": response.text}
    except Exception as e:
        logger.error(f"❌ Gemini API Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error calling Gemini: {e}")
