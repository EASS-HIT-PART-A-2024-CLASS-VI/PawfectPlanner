# File: backend/schemas.py

from pydantic import BaseModel, EmailStr, HttpUrl, validator
from typing import Optional, List
from datetime import date, datetime

#
# -- USER SCHEMAS --
#
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True


#
# -- PET SCHEMAS --
#
class PetBase(BaseModel):
    name: str
    type: str  # 'dog', 'cat', 'other'
    breed: str
    other_breed: Optional[str] = None
    birth_date: Optional[date] = None
    weight: Optional[float] = None
    health_issues: Optional[List[str]] = []
    behavior_issues: Optional[List[str]] = []
    pet_image_url: Optional[HttpUrl] = None

    # Additional breed-related data
    bred_for: Optional[str] = None
    breed_group: Optional[str] = None
    average_weight_range: Optional[str] = None
    life_expectancy: Optional[str] = None

    @validator("type")
    def validate_pet_type(cls, value):
        valid_types = {"dog", "cat", "other"}
        if value.lower() not in valid_types:
            raise ValueError(f"Pet type must be one of {valid_types}")
        return value

    @validator("breed", always=True)
    def validate_breed(cls, value, values):
        # If type == "other", we force breed to "other"
        if "type" in values and values["type"].lower() == "other":
            return "other"
        return value

    @validator("other_breed", always=True)
    def validate_other_breed(cls, value, values):
        # If breed == "other", must supply other_breed
        if values.get("breed") == "other" and not value:
            raise ValueError("When breed is 'other', other_breed must be provided.")
        # If breed != "other", other_breed must not be set
        if values.get("breed") != "other" and value:
            raise ValueError("other_breed is only valid if breed is 'other'.")
        return value

    @validator("weight", always=True)
    def validate_weight(cls, value, values):
        """
        Disallow negative weight for all pets.
        For dogs/cats, also disallow weight > 200 kg.
        """
        if value is not None:
            if value < 0:
                raise ValueError("Weight cannot be negative.")
            pet_type = values.get("type", "").lower()
            if pet_type in ["dog", "cat"] and value > 200:
                raise ValueError("Weight cannot exceed 200 kg for dogs/cats.")
        return value

    @validator("birth_date")
    def validate_birth_date(cls, value, values):
        """
        Disallow future birth dates for all pets.
        For dogs/cats, also disallow age > 50 years.
        """
        if value:
            today = date.today()
            # No future dates
            if value > today:
                raise ValueError("Birth date cannot be in the future.")
            # If dog/cat, max 50 years old
            pet_type = values.get("type", "").lower()
            if pet_type in ["dog", "cat"]:
                oldest_allowed = date(today.year - 50, today.month, today.day)
                if value < oldest_allowed:
                    raise ValueError("Birth date is too far in the past (max 50 years for dogs/cats).")
        return value

    class Config:
        from_attributes = True


class PetCreate(PetBase):
    owner_id: int  # match the DB column for ownership


class PetUpdate(PetBase):
    # All fields optional for partial updates
    name: Optional[str] = None
    type: Optional[str] = None
    breed: Optional[str] = None
    other_breed: Optional[str] = None
    birth_date: Optional[date] = None
    weight: Optional[float] = None
    health_issues: Optional[List[str]] = None
    behavior_issues: Optional[List[str]] = None
    bred_for: Optional[str] = None
    breed_group: Optional[str] = None
    average_weight_range: Optional[str] = None
    life_expectancy: Optional[str] = None


class PetResponse(PetBase):
    id: int
    owner_id: int

    # Convert comma-separated strings to lists
    @validator("health_issues", pre=True)
    def parse_health_issues(cls, value):
        if isinstance(value, str):
            return [v.strip() for v in value.split(",") if v.strip()]
        return value if value else []

    @validator("behavior_issues", pre=True)
    def parse_behavior_issues(cls, value):
        if isinstance(value, str):
            return [v.strip() for v in value.split(",") if v.strip()]
        return value if value else []

    class Config:
        from_attributes = True


#
# -- TREATMENT SCHEMAS --
#
class TreatmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    frequency: Optional[str] = None
    next_due_date: Optional[date] = None

    class Config:
        from_attributes = True

class TreatmentCreate(TreatmentBase):
    pet_id: int

class TreatmentUpdate(TreatmentBase):
    pass

class TreatmentResponse(TreatmentBase):
    id: int
    pet_id: int

    class Config:
        from_attributes = True


#
# -- REMINDER SCHEMAS --
#
class ReminderBase(BaseModel):
    title: str
    date: str  # "YYYY-MM-DD"
    time: str  # "HH:MM"
    repetition: str
    location: Optional[str] = None
    notes: Optional[str] = None

class ReminderCreate(ReminderBase):
    pet_id: Optional[int] = None

class ReminderUpdate(BaseModel):
    title: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    repetition: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None

class ReminderResponse(BaseModel):
    id: int
    pet_id: Optional[int] = None
    title: str
    due_date: datetime
    repetition: str
    location: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True
