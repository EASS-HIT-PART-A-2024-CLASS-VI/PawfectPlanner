# File: backend/main.py

import logging
logging.basicConfig(level=logging.INFO)

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

import models  
from database import init_db
from routes.pets import router as pets_router
from routes.reminders import router as reminders_router
from routes.treatments import router as treatments_router
from routes.breeds import router as breeds_router
from routes.auth import router as auth_router

app = FastAPI(title="Pawfect Planner API", version="1.0.0")

# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    # Only initialize the database if not in testing mode.
    if not os.getenv("TESTING"):
        init_db()

# Register routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(pets_router, prefix="/pets", tags=["Pets"])
app.include_router(reminders_router, prefix="/reminders", tags=["Reminders"])
app.include_router(treatments_router, prefix="/treatments", tags=["Treatments"])
app.include_router(breeds_router, prefix="/breeds", tags=["Breeds"])

@app.get("/")
def root():
    return {"message": "Welcome to Pawfect Planner API"}

if __name__ == "__main__":
    # Only used when running locally with: python backend/main.py
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
