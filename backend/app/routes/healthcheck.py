from fastapi import APIRouter

router = APIRouter()

@router.get("/healthcheck", tags=["Healthcheck"])
async def healthcheck():
    """
    Simple endpoint to check if the service is running.
    """
    return {"status": "ok", "message": "Service is up and running"}
