from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.concurrency import run_in_threadpool
from src.services.disease.predict import predict_disease
from src.core.config import settings


router = APIRouter(
    prefix=settings.crop_disease_detection_prefix,
    tags=["Crop Disease Detection"]
)


@router.post(
     "/detect",
     summary="Crop Disease Detection API",
     description="Endpoint for detecting crop diseases from images."
)
async def detect_crop_disease(image: UploadFile = File(..., description="Upload an image of the crop for disease detection.", example="crop.jpg")):
    """Detect crop diseases from uploaded images."""
    try:
        # validate content type
        if image.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Please upload a JPG or PNG image."
            )

        # read image bytes
        image_bytes = await image.read()

        if not image_bytes:
            raise HTTPException(
                status_code=400,
                detail="Empty image file."
            )

        # run prediction (CPU-bound → threadpool)
        result = await run_in_threadpool(
            predict_disease,
            image_bytes
        )

        return result

    except HTTPException:
        # re-raise known HTTP errors
        raise

    except ValueError as e:
        # preprocessing / image decode errors
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )

    except Exception as e:
        # unexpected server error
        raise HTTPException(
            status_code=500,
            detail=str(e)   # 👈 TEMPORARY
        )