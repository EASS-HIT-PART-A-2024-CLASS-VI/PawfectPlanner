# File: backend/tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.main import app
from backend.database import Base, get_db
from backend import models

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"  # in-memory for tests

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def override_get_db():
    """Use the test DB session instead of the real DB session."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create all tables in the in-memory DB once, then drop after tests."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    # Override get_db so that any route depending on get_db uses our test session
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
