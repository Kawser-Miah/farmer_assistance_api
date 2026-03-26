"""Fertilizer Recommendation API endpoint.

This module provides the REST API endpoint for fertilizer recommendations
based on crop, soil, and environmental conditions.
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.concurrency import run_in_threadpool
from src.core.jwt_validation import decode_supabase_jwt
from src.core.config import settings
from src.schemas.fertilizer_tips_schemas import FertilizerRequest, FertilizerResponse
from src.services.fertilizer_tips_service.predict import predict_fertilizer


router = APIRouter(
    prefix=settings.fertilizer_tips_prefix,
    tags=["Fertilizer Tips"]
)


@router.post(
    "/predict",
    response_model=FertilizerResponse,
    summary="Fertilizer Recommendation",
    description="Get fertilizer recommendation based on crop, soil, and environmental conditions."
)
async def predict_fertilizer_recommendation(
    request: FertilizerRequest,
    user_id: str = Depends(decode_supabase_jwt)
):
    """
    Predict the best fertilizer for given conditions.

    **Input features:**
    - crop: Name of the crop (e.g., 'Wheat', 'Rice', 'Maize')
    - soil_color: Color of the soil (e.g., 'Red', 'Black', 'Brown')
    - temperature: Temperature in Celsius
    - nitrogen: Nitrogen content in soil
    - potassium: Potassium content in soil
    - phosphorus: Phosphorus content in soil
    - rainfall: Rainfall in mm
    - ph: Soil pH level (0-14)

    **Returns:**
    - fertilizer: Recommended fertilizer name
    - confidence: Model confidence score
    - feature_importance: Top contributing features

    **Error handling:**
    - 422: Invalid input data (e.g., unknown crop or soil type)
    - 500: Model loading or prediction errors
    """
    try:
        # Run prediction in threadpool (CPU-bound operation)
        result = await run_in_threadpool(
            predict_fertilizer,
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
