"""Yield Estimation API endpoint.

This module provides the REST API endpoint for crop yield prediction
based on crop type, location, and environmental conditions.
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.concurrency import run_in_threadpool
from src.core.jwt_validation import decode_supabase_jwt
from src.core.config import settings
from src.schemas.yield_estimation_schemas import YieldEstimationRequest, YieldEstimationResponse
from src.services.yield_estimation_service.predict import predict_yield


router = APIRouter(
    prefix=settings.yield_estimation_prefix,
    tags=["Yield Estimation"]
)


@router.post(
    "/predict",
    response_model=YieldEstimationResponse,
    summary="Crop Yield Estimation",
    description="Predict crop yield based on crop type, location, and environmental conditions."
)
async def predict_crop_yield(
    request: YieldEstimationRequest,
    user_id: str = Depends(decode_supabase_jwt)
):
    """
    Predict crop yield for given conditions.

    **Input features:**
    - item: Crop type (e.g., 'Maize', 'Wheat', 'Rice')
    - area: Country/region where crop is grown (e.g., 'Brazil', 'India', 'USA')
    - rainfall: Annual rainfall in mm
    - temperature: Average temperature in Celsius
    - pesticides: Pesticides used in tonnes

    **Returns:**
    - predicted_yield: Estimated crop yield in t/ha (tonnes per hectare)
    - item: Echo of crop type
    - area: Echo of area/region
    - confidence: Model confidence score
    - feature_importance: Top contributing features

    **Error handling:**
    - 422: Invalid input data (e.g., unknown crop or area)
    - 500: Model loading or prediction errors
    """
    try:
        # Run prediction in threadpool (CPU-bound operation)
        result = await run_in_threadpool(
            predict_yield,
            request
        )
        return result

    except FileNotFoundError as e:
        print(f"❌ Model file not found: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Model file not found: {str(e)}"
        )

    except ValueError as e:
        print(f"⚠️ Value error during prediction: {str(e)}")
        raise HTTPException(
            status_code=422,
            detail=f"Invalid input data: {str(e)}"
        )

    except Exception as e:
        print(f"❌ Unexpected error during prediction: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )
