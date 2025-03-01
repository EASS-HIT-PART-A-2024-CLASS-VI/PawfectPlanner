from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes.pets import router as pets_router
from app.routes.reminders import router as reminders_router
from app.routes.treatments import router as treatments_router
from app.routes.breeds import router as breeds_router
from app.routes.auth import router as auth_router
import uvicorn

# Initialize FastAPI app
app = FastAPI(title="Pawfect Planner API", version="1.0.0")

# ✅ Fix CORS (Allow frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Ensure database tables exist
Base.metadata.create_all(bind=engine)

# ✅ Fix API prefixes
app.include_router(auth_router, tags=["Auth"])  # 🔧 Remove prefix here
app.include_router(pets_router, prefix="/api/pets", tags=["Pets"])
app.include_router(reminders_router, prefix="/api/reminders", tags=["Reminders"])
app.include_router(treatments_router, prefix="/api/treatments", tags=["Treatments"])
app.include_router(breeds_router, prefix="/api/breeds", tags=["Breeds"])

@app.get("/")
def root():
    return {"message": "Welcome to Pawfect Planner API"}

# ✅ Ensure proper startup inside Docker
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
