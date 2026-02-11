from fastapi import APIRouter
from src.core.config import settings

router = APIRouter(
    prefix=settings.crop_disease_detection_prefix,
    tags=["Crop Disease Detection"]
)

@router.get(
     "/predict",
     summary="Crop Disease Detection API",
     description="Endpoint for detecting crop diseases from images."
)
async def detect_crop_disease():
    """Detect crop diseases from uploaded images."""
    return {
        "message": "Crop disease detection endpoint is under construction."
    }