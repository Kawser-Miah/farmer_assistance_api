from fastapi import APIRouter, HTTPException, Depends
from src.core.jwt_validation import decode_supabase_jwt
from src.core.config import settings
from src.schemas.smart_irrigation_schemas import IrrigationRequest, IrrigationResponse
from src.services.smart_irrigation_services.predict import predict_irrigation


router = APIRouter(
    prefix=settings.smart_irrigation_prefix,
    tags=["Smart Irrigation"]
)


@router.post(
    "/predict",
    response_model=IrrigationResponse,
    summary="Smart Irrigation Prediction",
    description="Predict whether irrigation is needed based on crop, soil, and environmental conditions."
)
async def predict_irrigation_need(
    request: IrrigationRequest,
    user_id: str = Depends(decode_supabase_jwt)
):
    """
    Predict irrigation need based on input features.

    **Input features:**
    - crop_id: ID of the crop
    - soil_type: Encoded soil type
    - seedling_stage: Current seedling stage
    - moi: Soil moisture percentage (0-100)
    - temp: Temperature in Celsius
    - humidity: Humidity percentage (0-100)

    **Returns:**
    - irrigation_needed: Boolean indicating if irrigation is needed
    - recommendation: Human-readable recommendation
    - confidence: Model confidence score
    - input_features: Echo of input features for verification
    """
    try:
        result = predict_irrigation(request)
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
