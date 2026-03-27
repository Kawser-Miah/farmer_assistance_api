from pydantic import BaseModel, Field


class IrrigationRequest(BaseModel):
    """Request model for smart irrigation prediction."""
    crop_id: str = Field(...,  example="Wheat", description="Crop ID")
    soil_type: str = Field(...,  example="Clay Soil", description="Soil type (encoded)")
    seedling_stage: str = Field(...,  example="Vegetative Growth / Root or Tuber Development", description="Seedling stage")
    moi: float = Field(..., ge=0, le=100, example=40.0, description="Soil moisture (%)")
    temp: float = Field(..., example=30.0, description="Temperature (°C)")
    humidity: float = Field(..., ge=0, le=100, example=60.0, description="Humidity (%)")


class IrrigationResponse(BaseModel):
    """Response model for smart irrigation prediction."""
    irrigation_needed: bool = Field(..., example=True, description="Whether irrigation is needed")
    recommendation: str = Field(..., example="💧 Irrigation Needed", description="Human-readable recommendation")
    confidence: float = Field(..., ge=0, le=1, example=0.95, description="Model confidence score (if available)")
    feature_importance: dict = Field(..., description="Feature importance scores")
