"""Crop Recommendation API endpoint.

This module provides the REST API endpoint for crop recommendations
based on soil nutrients and environmental conditions.
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.concurrency import run_in_threadpool
from src.core.jwt_validation import decode_supabase_jwt
from src.core.config import settings
from src.schemas.crop_recommendation_schemas import CropRecommendationRequest, CropRecommendationResponse
from src.services.crop_recommendation.predict import predict_crop


router = APIRouter(
    prefix=settings.crop_recommendation_prefix,
    tags=["Crop Recommendation"]
)


@router.post(
    "/predict",
    response_model=CropRecommendationResponse,
    summary="Crop Recommendation",
    description="Get crop recommendation based on soil nutrients and environmental conditions."
)
async def predict_crop_recommendation(
    request: CropRecommendationRequest,
    user_id: str = Depends(decode_supabase_jwt)
):
    """
    Predict the best crop for given conditions.

    **Input features:**
    - nitrogen: Nitrogen content in soil
    - phosphorus: Phosphorus content in soil
    - potassium: Potassium content in soil
    - temperature: Temperature in Celsius
    - humidity: Humidity percentage (0-100)
    - ph: Soil pH level (0-14)
    - rainfall: Rainfall in mm

    **Returns:**
    - crop: Recommended crop name
    - confidence: Model confidence score
    - feature_importance: Top contributing features

    **Error handling:**
    - 422: Invalid input data
    - 500: Model loading or prediction errors
    """
    try:
        # Run prediction in threadpool (CPU-bound operation)
        result = await run_in_threadpool(
            predict_crop,
            request
        )
        return result

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Model file not found: {str(e)}"
        )

    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid input data: {str(e)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )
