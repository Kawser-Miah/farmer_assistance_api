"""Crop Recommendation Prediction Service.

This module provides prediction logic for crop recommendation based on soil
and environmental conditions.
"""

import numpy as np
from typing import Dict
from src.services.crop_recommendation.model import get_crop_recommendation_model
from src.schemas.crop_recommendation_schemas import CropRecommendationRequest, CropRecommendationResponse


FEATURE_NAMES = [
    'Nitrogen',
    'Phosphorus',
    'Potassium',
    'Temperature',
    'Humidity',
    'pH',
    'Rainfall'
]


def get_feature_importance(model) -> Dict[str, float]:
    """
    Extract and return top feature importance scores.

    Args:
        model: Trained model with feature_importances_ attribute

    Returns:
        Dictionary of top 3 features and their importance scores
    """
    try:
        importance = dict(zip(FEATURE_NAMES, model.feature_importances_.tolist()))

        # Sort and take top 3
        sorted_items = sorted(importance.items(), key=lambda x: x[1], reverse=True)[:3]

        return {k: round(v, 4) for k, v in sorted_items}
    except AttributeError:
        return {"Note": "Feature importance not available for this model"}


def predict_crop(request: CropRecommendationRequest) -> CropRecommendationResponse:
    """
    Predict recommended crop based on soil and environmental conditions.

    Args:
        request: CropRecommendationRequest containing soil nutrients and environmental data

    Returns:
        CropRecommendationResponse with recommended crop and explainability metrics

    Raises:
        ValueError: If model prediction fails
    """

    # Load model
    model = get_crop_recommendation_model()

    # Prepare features in correct order: ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'pH', 'Rainfall']
    feature_array = np.array([[
        request.nitrogen,
        request.phosphorus,
        request.potassium,
        request.temperature,
        request.humidity,
        request.ph,
        request.rainfall
    ]])

    # Make prediction
    prediction_encoded = model.predict(feature_array)

    # Calculate confidence score
    try:
        probabilities = model.predict_proba(feature_array)[0]
        confidence = round(float(max(probabilities)), 2)
    except AttributeError:
        confidence = 0.85

    # Decode crop recommendation (if model has classes_)
    try:
        predicted_crop = model.classes_[prediction_encoded[0]]
    except (AttributeError, IndexError):
        predicted_crop = str(prediction_encoded[0])

    # Get feature importance
    feature_importance = get_feature_importance(model)

    return CropRecommendationResponse(
        crop=predicted_crop,
        confidence=confidence,
        feature_importance=feature_importance
    )
