from fastapi import APIRouter, HTTPException
from functools import lru_cache
import json
import logging
from datetime import datetime, timedelta

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Supported pet types
VALID_PET_TYPES = ["cat", "dog"]

def validate_pet_type(pet_type: str):
    """
    Validate the pet type input.
    """
    if pet_type.lower() not in VALID_PET_TYPES:
        logging.error(f"Invalid pet type provided: {pet_type}")
        raise HTTPException(status_code=400, detail=f"Unsupported pet type: {pet_type}. Must be one of {VALID_PET_TYPES}.")

@lru_cache(maxsize=10)
def load_vaccine_data(pet_type: str):
    """
    Load vaccine data from the JSON file, with caching for efficiency.
    """
    file_path = f"data/{pet_type}_vaccines.json"
    try:
        with open(file_path, "r") as file:
            logging.info(f"Loading vaccine data for {pet_type}.")
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise HTTPException(status_code=404, detail="Vaccination data not found.")

def get_description(vaccine_name: str, language: str = "en"):
    """
    Fetch the vaccine description in the specified language.
    """
    try:
        with open("data/vaccines_lang.json", "r") as lang_file:
            lang_data = json.load(lang_file)
            return lang_data.get(language, {}).get(vaccine_name, "")
    except FileNotFoundError:
        logging.warning("Language file not found. Defaulting to hardcoded descriptions.")
        return ""

@router.get("/vaccines")
def get_vaccines(pet_type: str, criticality: str = None):
    """
    Fetch vaccination data for dogs or cats.
    Optionally filter by criticality (mandatory/recommended).
    """
    validate_pet_type(pet_type)
    vaccine_data = load_vaccine_data(pet_type)
    
    if criticality:
        criticality = criticality.lower()
        if criticality not in ["mandatory", "recommended"]:
            raise HTTPException(status_code=400, detail="Invalid criticality value. Must be 'mandatory' or 'recommended'.")
        return vaccine_data.get(criticality, [])

    return vaccine_data

@router.post("/vaccines/schedule")
def calculate_vaccine_schedule(birth_date: str, pet_type: str, language: str = "en"):
    """
    Calculate a vaccination schedule based on the pet's age.
    """
    validate_pet_type(pet_type)

    try:
        # Load vaccination data
        vaccine_data = load_vaccine_data(pet_type)
        
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
        today = datetime.today()

        schedule = []
        for vaccine in vaccine_data.get("recommended", []):
            if "puppy_schedule" in vaccine or "kitten_schedule" in vaccine:
                schedule_key = "puppy_schedule" if pet_type == "dog" else "kitten_schedule"
                for weeks in vaccine.get(schedule_key, []):
                    due_date = birth_date + timedelta(weeks=int(weeks.split()[0]))
                    if due_date > today:
                        schedule.append({
                            "name": vaccine["name"],
                            "due_date": due_date.strftime("%Y-%m-%d"),
                            "description": f"{get_description(vaccine['name'], language)}"
                        })
            else:
                interval = int(vaccine["frequency"].split()[0])
                next_due_date = birth_date + timedelta(weeks=interval * 52)
                while next_due_date <= today:
                    next_due_date += timedelta(weeks=interval * 52)
                schedule.append({
                    "name": vaccine["name"],
                    "due_date": next_due_date.strftime("%Y-%m-%d"),
                    "description": f"{get_description(vaccine['name'], language)}"
                })
        return {"schedule": schedule}
    except Exception as e:
        logging.error(f"Error generating schedule: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating schedule: {str(e)}")
