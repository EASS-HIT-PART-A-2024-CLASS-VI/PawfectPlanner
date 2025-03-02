# models.py
from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    pets = relationship("Pet", back_populates="owner")

class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # 'dog', 'cat', or 'other'
    breed = Column(String, nullable=True)  # 'other' or specific breed
    other_breed = Column(String, nullable=True)  # user-defined breed
    birth_date = Column(DateTime, nullable=True)  # or Date if you prefer
    weight = Column(Float, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="pets")

class Treatment(Base):
    __tablename__ = "treatments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    frequency = Column(String, nullable=True)
    next_due_date = Column(DateTime, nullable=True)
    pet_id = Column(Integer, ForeignKey("pets.id"))

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # Changed to DateTime so we can store both date & time
    due_date = Column(DateTime, nullable=False)

    pet_id = Column(Integer, ForeignKey("pets.id"))
