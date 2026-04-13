from pydantic import BaseModel, Field


class CropRecommendationRequest(BaseModel):
    """Request model for crop recommendation."""
    nitrogen: float = Field(..., ge=0, example=90.0, description="Nitrogen content in soil")
    phosphorus: float = Field(..., ge=0, example=42.0, description="Phosphorus content in soil")
    potassium: float = Field(..., ge=0, example=43.0, description="Potassium content in soil")
    temperature: float = Field(..., example=20.87, description="Temperature in Celsius")
    humidity: float = Field(..., ge=0, le=100, example=82.0, description="Humidity percentage (0-100)")
    ph: float = Field(..., ge=0, le=14, example=6.5, description="Soil pH level (0-14)")
    rainfall: float = Field(..., ge=0, example=202.93, description="Rainfall in mm")


class CropRecommendationResponse(BaseModel):
    """Response model for crop recommendation."""
    crop: str = Field(..., example="Jute", description="Recommended crop name")
    confidence: float = Field(..., ge=0, le=1, example=0.95, description="Model confidence score")
    # feature_importance: dict = Field(..., description="Top contributing features and their importance scores")
