from pydantic import BaseModel, EmailStr, HttpUrl, validator
from typing import Optional, List
from datetime import date


# User Schemas
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(UserBase):
    password: str


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


# Pet Schemas
class PetBase(BaseModel):
    name: str
    type: str  # 'dog', 'cat', or 'other'
    breed: str
    other_breed: Optional[str] = None
    birth_date: Optional[date] = None
    weight: Optional[float] = None
    health_issues: Optional[List[str]] = []
    behavior_issues: Optional[List[str]] = []
    pet_image_url: Optional[HttpUrl] = None

    @validator("type")
    def validate_pet_type(cls, value):
        valid_types = {"dog", "cat", "other"}
        if value.lower() not in valid_types:
            raise ValueError(f"Pet type must be one of {valid_types}.")
        return value

    @validator("breed", always=True)
    def validate_breed(cls, value, values):
        if "type" in values and values["type"].lower() == "other":
            return "other"
        return value

    @validator("other_breed", always=True)
    def validate_other_breed(cls, value, values):
        if values.get("breed") == "other" and not value:
            raise ValueError("When breed is 'other', other_breed must be provided.")
        if values.get("breed") != "other" and value:
            raise ValueError("other_breed should only be set if breed is 'other'.")
        return value

    @validator("weight", always=True)
    def validate_weight(cls, value):
        if value is not None and value <= 0:
            raise ValueError("Weight must be greater than 0.")
        return value

    class Config:
        orm_mode = True


class PetCreate(PetBase):
    owner_id: int


class PetUpdate(PetBase):
    pass


class PetResponse(PetBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


# Treatment Schemas
class TreatmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    frequency: Optional[str] = None
    next_due_date: Optional[date] = None


class TreatmentCreate(TreatmentBase):
    pet_id: int


class TreatmentUpdate(TreatmentBase):
    pass


class TreatmentResponse(TreatmentBase):
    id: int
    pet_id: int

    class Config:
        orm_mode = True


# Reminder Schemas
class ReminderBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: date


class ReminderCreate(ReminderBase):
    pet_id: int


class ReminderUpdate(ReminderBase):
    pass


class ReminderResponse(ReminderBase):
    id: int
    pet_id: int

    class Config:
        orm_mode = True
