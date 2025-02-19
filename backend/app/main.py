from fastapi import FastAPI
from app.database import engine, Base
from app.routes.pets import router as pets_router
from app.routes.reminders import router as reminders_router
from app.routes.treatments import router as treatments_router
from app.routes.breeds import router as breeds_router

# Initialize FastAPI app
app = FastAPI(title="Pawfect Planner API", version="1.0.0")

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(pets_router, prefix="/pets", tags=["Pets"])
app.include_router(reminders_router, prefix="/reminders", tags=["Reminders"])
app.include_router(treatments_router, prefix="/treatments", tags=["Treatments"])
app.include_router(breeds_router, prefix="/breeds", tags=["Breeds"])

@app.get("/")
def root():
    return {"message": "Welcome to Pawfect Planner API"}
