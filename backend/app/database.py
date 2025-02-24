from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Ensure the correct database URL is used
DATABASE_URL = "postgresql://user:password@db:5432/pets_db"

# Create the SQLAlchemy engine without SQLite-specific options
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
