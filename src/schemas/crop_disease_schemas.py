from pydantic import BaseModel, Field

class DiseasePredictionResponse(BaseModel):
    label: str = Field(..., example="Tomato_Late_blight")
    confidence: float = Field(..., example=96.42)
    heatmap_url: str = Field(..., example="media/gradcam/heatmap_12345.png")
