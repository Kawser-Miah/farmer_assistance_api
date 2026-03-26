from pydantic import BaseModel, Field


class FertilizerRequest(BaseModel):
    """Request model for fertilizer recommendation."""
    crop: str = Field(..., example="Wheat", description="Crop name")
    soil_color: str = Field(..., example="Red", description="Soil color")
    temperature: float = Field(..., example=25.0, description="Temperature in Celsius")
    nitrogen: float = Field(..., ge=0, example=80.0, description="Nitrogen content in soil")
    potassium: float = Field(..., ge=0, example=40.0, description="Potassium content in soil")
    phosphorus: float = Field(..., ge=0, example=40.0, description="Phosphorus content in soil")
    rainfall: float = Field(..., ge=0, example=100.0, description="Rainfall in mm")
    ph: float = Field(..., ge=0, le=14, example=6.5, description="Soil pH level (0-14)")


class FertilizerResponse(BaseModel):
    """Response model for fertilizer recommendation."""
    fertilizer: str = Field(..., example="Urea", description="Recommended fertilizer name")
    confidence: float = Field(..., ge=0, le=1, example=0.95, description="Model confidence score (if available)")
    feature_importance: dict = Field(..., description="Top contributing features and their importance scores")
