from fastapi import APIRouter

router = APIRouter()

@router.get("/local-services/vet")
def find_nearby_vets():
    """
    Returns a Google Maps search link for nearby veterinary services.
    """
    return {
        "message": "Find nearby vets using the link below:",
        "link": "https://www.google.com/maps/search/vet+services"
    }

@router.get("/local-services/grooming")
def find_nearby_grooming():
    """
    Returns a Google Maps search link for nearby pet grooming services.
    """
    return {
        "message": "Find nearby pet grooming services using the link below:",
        "link": "https://www.google.com/maps/search/pet+grooming"
    }
