from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from src.core.jwt_validation import decode_supabase_jwt
from fastapi.concurrency import run_in_threadpool
from src.services.disease.predict import predict_disease
from src.core.config import settings
from src.core.database import supabase


router = APIRouter(
    prefix=settings.crop_disease_detection_prefix,
    tags=["Crop Disease Detection"]
)


@router.post(
     "/detect",
     summary="Crop Disease Detection API",
     description="Endpoint for detecting crop diseases from images."
)
async def detect_crop_disease(user_id: str = Depends(decode_supabase_jwt),
    image: UploadFile = File(..., description="Upload an image of the crop for disease detection.", example="crop.jpg")):
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
            image_bytes,
            user_id
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

@router.get(
    "/test-users",
    summary="Test Supabase Connection",
    description="Simple test endpoint to fetch users from Supabase."
)
async def test_users():
    """Test endpoint to verify Supabase connection."""
    try:
        response = supabase.table("users").select("*").execute()
        
        return {
            "success": True,
            "count": len(response.data),
            "data": response.data
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch users: {str(e)}"
        )
