# File: backend/app/models.py

from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    # pets = relationship("Pet", back_populates="owner")

class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # 'dog', 'cat', 'other'
    breed = Column(String, nullable=True)  # 'other' or specific breed
    other_breed = Column(String, nullable=True)
    birth_date = Column(DateTime, nullable=True)
    weight = Column(Float, nullable=True)

    # Breed metadata
    average_weight_range = Column(String, nullable=True)
    life_expectancy = Column(String, nullable=True)
    temperament = Column(String, nullable=True)
    bred_for = Column(String, nullable=True)
    breed_group = Column(String, nullable=True)

    # Store health/behavior issues as comma-separated strings
    health_issues = Column(String, nullable=True)
    behavior_issues = Column(String, nullable=True)

    # Link to the user’s ID
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)

class Treatment(Base):
    __tablename__ = "treatments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    frequency = Column(String, nullable=True)
    next_due_date = Column(DateTime, nullable=True)
    pet_id = Column(Integer)  # or ForeignKey("pets.id") if you prefer

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=False)
    repeat = Column(String, nullable=True)   # For repeated reminders
    location = Column(String, nullable=True)
    pet_id = Column(Integer)
