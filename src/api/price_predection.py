"""Price Prediction API endpoint.

This module provides the REST API endpoint for commodity price predictions
based on market data, temporal features, and location information.
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.concurrency import run_in_threadpool
from src.core.jwt_validation import decode_supabase_jwt
from src.core.config import settings
from src.schemas.price_predection_schemas import PricePredictionRequest, PricePredictionResponse
from src.services.price_predection.predict import predict_price


router = APIRouter(
    prefix=settings.price_predection_prefix,
    tags=["Price Prediction"]
)


@router.post(
    "/predict",
    response_model=PricePredictionResponse,
    summary="Price Prediction",
    description="Predict commodity price in a given market, date, and conditions."
)
async def predict_commodity_price(
    request: PricePredictionRequest,
    # user_id: str = Depends(decode_supabase_jwt)
):
    """
    Predict commodity price (BDT) for given market and temporal conditions.

    **Input features:**
    - date: Date in YYYY-MM-DD format
    - admin1: Administrative division level 1 (e.g., 'Dhaka')
    - admin2: Administrative division level 2 (e.g., 'Dhaka')
    - market: Market name (e.g., 'Dhaka (Karwan Bazar)')
    - latitude: Latitude coordinate (float)
    - longitude: Longitude coordinate (float)
    - category: Product category (e.g., 'cereals and tubers')
    - commodity: Commodity name (e.g., 'Rice (coarse)')
    - unit: Unit of measurement (e.g., 'KG')
    - priceflag: Price flag (e.g., 'actual')
    - pricetype: Price type (e.g., 'Retail')

    **Returns:**
    - predicted_price: Predicted price in BDT per unit
    - commodity: Commodity name
    - market: Market name
    - unit: Unit of measurement
    - date: Date of prediction

    **Error handling:**
    - 422: Invalid input data or unsupported market/commodity
    - 500: Model loading or prediction errors
    """
    try:
        # Run prediction in threadpool (CPU-bound operation)
        result = await run_in_threadpool(
            predict_price,
            request
        )
        return result

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Model bundle file not found: {str(e)}"
        )

    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid input data: {str(e)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Price prediction failed: {str(e)}"
        )
