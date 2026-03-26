import numpy as np
from typing import Dict
from src.services.fertilizer_tips_service.model import (
    get_fertilizer_model,
    get_fertilizer_encoder,
    get_crop_encoder,
    get_soil_encoder
)
from src.schemas.fertilizer_tips_schemas import FertilizerRequest, FertilizerResponse


FEATURE_NAMES = [
    'Crop',
    'Soil_color',
    'Temperature',
    'Nitrogen',
    'Potassium',
    'Phosphorus',
    'Rainfall',
    'pH'
]


def get_feature_importance(model) -> Dict[str, float]:
    """
    Extract and return top feature importance
    """
    importance = dict(zip(FEATURE_NAMES, model.feature_importances_.tolist()))

    # Sort and take top 3 (clean output like your irrigation example)
    sorted_items = sorted(importance.items(), key=lambda x: x[1], reverse=True)[:3]

    return {k: round(v, 2) for k, v in sorted_items}


def predict_fertilizer(request: FertilizerRequest) -> FertilizerResponse:
    """
    Predict fertilizer with simple explainability
    """

    # Load model and encoders
    model = get_fertilizer_model()
    le_fertilizer = get_fertilizer_encoder()
    le_crop = get_crop_encoder()
    le_soil = get_soil_encoder()

    # Encode categorical features
    try:
        crop_encoded = le_crop.transform([request.crop])[0]
        soil_encoded = le_soil.transform([request.soil_color])[0]
    except ValueError as e:
        raise ValueError(f"Invalid crop or soil color: {str(e)}")

    # Feature dictionary
    feature_dict = {
        'Crop': crop_encoded,
        'Soil_color': soil_encoded,
        'Temperature': request.temperature,
        'Nitrogen': request.nitrogen,
        'Potassium': request.potassium,
        'Phosphorus': request.phosphorus,
        'Rainfall': request.rainfall,
        'pH': request.ph
    }

    # Ensure correct order
    model_features = model.feature_names_in_
    feature_array = np.array([[feature_dict[f] for f in model_features]])

    # Prediction
    prediction_encoded = model.predict(feature_array)

    # Confidence
    try:
        probabilities = model.predict_proba(feature_array)[0]
        confidence = round(float(max(probabilities)), 2)
    except AttributeError:
        confidence = 1.0

    # Decode fertilizer
    predicted_fertilizer = le_fertilizer.inverse_transform(prediction_encoded)[0]

    # ✅ Explainability (same style as irrigation)
    feature_importance = get_feature_importance(model)

    return FertilizerResponse(
        fertilizer=predicted_fertilizer,
        confidence=confidence,
        feature_importance=feature_importance
    )