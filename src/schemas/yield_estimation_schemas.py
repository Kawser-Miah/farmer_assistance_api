from pydantic import BaseModel, Field


class YieldEstimationRequest(BaseModel):
    """Request model for crop yield estimation."""
    item: str = Field(..., example="Maize", description="Crop type (e.g., 'Maize', 'Wheat', 'Rice')")
    area: str = Field(..., example="Brazil", description="Country/region where crop is grown")
    rainfall: float = Field(..., ge=0, example=1300.0, description="Annual rainfall in mm")
    temperature: float = Field(..., example=28.5, description="Average temperature in Celsius")
    pesticides: float = Field(..., ge=0, example=1800.0, description="Pesticides used in tonnes")


class YieldEstimationResponse(BaseModel):
    """Response model for crop yield estimation."""
    predicted_yield: float = Field(..., example=5.20, description="Predicted crop yield in t/ha (tonnes per hectare)")
    yield_unit: str = Field(default="t/ha", example="t/ha", description="Unit of predicted_yield")
    item: str = Field(..., example="Maize", description="Crop type")
    area: str = Field(..., example="Brazil", description="Country/region")
    confidence: float = Field(..., ge=0, le=1, example=0.95, description="Model confidence score")
    feature_importance: dict = Field(..., description="Top contributing features and their importance scores")
