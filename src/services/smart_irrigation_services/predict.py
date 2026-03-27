import numpy as np
from typing import Dict
from src.services.smart_irrigation_services.model import get_irrigation_model, get_irrigation_soil_encoder, get_irrigation_crop_encoder, get_irrigation_stage_encoder
from src.schemas.smart_irrigation_schemas import IrrigationRequest, IrrigationResponse


FEATURE_NAMES = [
    "crop_id",
    "soil_type",
    "seedling_stage",
    "moisture",
    "temperature",
    "humidity"
]


def get_feature_importance(model) -> Dict[str, float]:
    importance = dict(zip(FEATURE_NAMES, model.feature_importances_.tolist()))

    # Sort & take top 3
    sorted_items = sorted(importance.items(), key=lambda x: x[1], reverse=True)[:3]

    return {k: round(v, 2) for k, v in sorted_items}


def predict_irrigation(request: IrrigationRequest) -> IrrigationResponse:
    """
    Predict irrigation need (minimal response)
    """

    # Load model
    model = get_irrigation_model()
    soil_encoder = get_irrigation_soil_encoder()
    crop_encoder = get_irrigation_crop_encoder()
    stage_encoder = get_irrigation_stage_encoder()
    # Encode categorical features
    try:
        soil_encoded = soil_encoder.transform([request.soil_type])[0]
    except Exception as e:
        print(f"Error encoding soil type: {e}")
        soil_encoded = 0

    try:
        crop_encoded = crop_encoder.transform([request.crop_id])[0]
    except Exception as e:
        print(f"Error encoding crop id: {e}")
        crop_encoded = 0

    try:
        stage_encoded = stage_encoder.transform([request.seedling_stage])[0]
    except Exception as e:
        print(f"Error encoding seedling stage: {e}")
        stage_encoded = 0

    # Prepare features
    features = np.array([[
        crop_encoded,
        soil_encoded,
        stage_encoded,
        request.moi,
        request.temp,
        request.humidity
    ]])

    # Prediction
    prediction = model.predict(features)[0]

    # Confidence
    try:
        probabilities = model.predict_proba(features)[0]
        confidence = round(float(max(probabilities)), 2)
    except AttributeError:
        confidence = 1.0

    irrigation_needed = bool(prediction == 1)
    recommendation = "💧 Irrigation Needed" if irrigation_needed else "✅ No Irrigation Needed"

    # ✅ Only feature importance
    feature_importance = get_feature_importance(model)

    return IrrigationResponse(
        irrigation_needed=irrigation_needed,
        recommendation=recommendation,
        confidence=confidence,
        feature_importance=feature_importance
    )