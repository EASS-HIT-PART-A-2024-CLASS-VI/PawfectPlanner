from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables.")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Configure session handling
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declare the base class for models
Base = declarative_base()

# Dependency function for database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
