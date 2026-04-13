from pydantic import BaseModel, Field


class PricePredictionRequest(BaseModel):
    """Request model for price prediction."""
    date: str = Field(..., example="2025-09-15", description="Date in format YYYY-MM-DD")
    admin1: str = Field(..., example="Dhaka", description="Administrative division level 1")
    admin2: str = Field(..., example="Dhaka", description="Administrative division level 2")
    market: str = Field(..., example="Dhaka (Karwan Bazar)", description="Market name")
    latitude: float = Field(..., example=23.81, description="Latitude coordinate")
    longitude: float = Field(..., example=90.41, description="Longitude coordinate")
    category: str = Field(..., example="cereals and tubers", description="Product category")
    commodity: str = Field(..., example="Rice (coarse)", description="Commodity name")
    unit: str = Field(..., example="KG", description="Unit of measurement")
    priceflag: str = Field(..., example="actual", description="Price flag (e.g., 'actual')")
    pricetype: str = Field(..., example="Retail", description="Price type (e.g., 'Retail', 'Wholesale')")


class PricePredictionResponse(BaseModel):
    """Response model for price prediction."""
    predicted_price: float = Field(..., example=45.50, description="Predicted price in BDT per unit")
    commodity: str = Field(..., example="Rice (coarse)", description="Commodity name")
    market: str = Field(..., example="Dhaka (Karwan Bazar)", description="Market name")
    unit: str = Field(..., example="KG", description="Unit of measurement")
    date: str = Field(..., example="2025-09-15", description="Date of prediction")
