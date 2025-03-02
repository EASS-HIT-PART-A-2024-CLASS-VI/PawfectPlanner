from fastapi import FastAPI, HTTPException, Request
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DOG_API_KEY = os.getenv("DOG_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Use these keys in your application logic
print(f"Dog API Key: {DOG_API_KEY}")
print(f"Gemini API Key: {GEMINI_API_KEY}")
