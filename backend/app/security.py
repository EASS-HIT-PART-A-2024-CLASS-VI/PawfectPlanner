import os
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve sensitive values securely
SECRET_KEY = os.getenv("SECRET_KEY", "your_fallback_secret_key")  # Fallback in case it's not set
SECRET_PEPPER = os.getenv("SECRET_PEPPER", "default_pepper_value")  # Extra security layer
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # Allows configuration

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies the password against the stored hashed password.
    Appends a secret pepper for extra security.
    """
    return pwd_context.verify(plain_password + SECRET_PEPPER, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hashes the password using bcrypt and appends a secret pepper for added security.
    """
    return pwd_context.hash(password + SECRET_PEPPER)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Creates a JWT access token with an expiration time.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    Decodes a JWT access token and verifies its authenticity.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
