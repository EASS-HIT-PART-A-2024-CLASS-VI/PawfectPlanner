# File: backend/routes/auth.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import EmailStr
from models import User
from schemas import UserCreate, UserLogin
from security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token
)
from database import get_db
from fastapi.security import OAuth2PasswordBearer
import os

# Load environment variables
DEBUG_MODE = os.getenv("DEBUG", "false").lower() == "true"

router = APIRouter(tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user with better error handling.
    """
    # Ensure password meets length requirement
    if len(user.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long.")

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    try:
        hashed_password = get_password_hash(user.password)
        new_user = User(email=user.email, password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User registered successfully"}
    except Exception as e:
        db.rollback()
        error_msg = "Database error occurred. Please try again later."
        if DEBUG_MODE:
            error_msg += f" [Debug: {str(e)}]"
        raise HTTPException(status_code=500, detail=error_msg)

@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate a user and generate a JWT token.
    """
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    try:
        token = create_access_token({"sub": db_user.email})
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        error_msg = "Token generation failed."
        if DEBUG_MODE:
            error_msg += f" [Debug: {str(e)}]"
        raise HTTPException(status_code=500, detail=error_msg)

@router.get("/me")
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Retrieve logged-in user details using JWT, including user.id.
    """
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_email = payload.get("sub")
    db_user = db.query(User).filter(User.email == user_email).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"email": str(db_user.email), "id": db_user.id}
