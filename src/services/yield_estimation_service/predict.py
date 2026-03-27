import numpy as np
from typing import Dict
from src.services.yield_estimation_service.model import (
    get_yield_model,
    get_item_encoder,
    get_area_encoder
)
from src.schemas.yield_estimation_schemas import YieldEstimationRequest, YieldEstimationResponse


FEATURE_NAMES = [
    'Item',
    'Area',
    'Rainfall',
    'Temperature',
    'Pesticides'
]

HG_PER_TON = 10000


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

        return {k: round(v, 2) for k, v in sorted_items}
    except AttributeError:
        # Model doesn't have feature_importances_ (e.g., linear regression)
        return {"Note": "Feature importance not available for this model"}


def predict_yield(request: YieldEstimationRequest) -> YieldEstimationResponse:
    """
    Predict crop yield based on input features.

    Args:
        request: YieldEstimationRequest containing crop, area, and environmental data

    Returns:
        YieldEstimationResponse with predicted yield and explainability metrics

    Raises:
        ValueError: If crop item or area is not in encoder's training categories
    """

    # Load model and encoders
    model = get_yield_model()
    le_item = get_item_encoder()
    le_area = get_area_encoder()

    # Encode categorical features
    try:
        item_encoded = le_item.transform([request.item])[0]
        area_encoded = le_area.transform([request.area])[0]
    except ValueError as e:
        raise ValueError(
            f"Invalid crop item or area. '{request.item}' or '{request.area}' "
            f"not found in training data categories. Error: {str(e)}"
        )

    # Prepare features in correct order: ['Item', 'Area', 'Rainfall', 'Temperature', 'Pesticides']
    feature_array = np.array([[
        item_encoded,
        area_encoded,
        request.rainfall,
        request.temperature,
        request.pesticides
    ]])

    # Make prediction in original model unit (hg/ha) and convert to human-readable t/ha.
    predicted_yield_hg_ha = model.predict(feature_array)[0]
    predicted_yield_t_ha = float(predicted_yield_hg_ha) / HG_PER_TON

    # Calculate confidence score
    try:
        # For regression models, we use R² score or similar
        # Since we don't have probabilities, we'll use a placeholder confidence
        # In production, you might want to calculate prediction intervals
        confidence = 0.85  # Default confidence for regression models
    except AttributeError:
        confidence = 0.85

    # Get feature importance
    feature_importance = get_feature_importance(model)

    return YieldEstimationResponse(
        predicted_yield=round(predicted_yield_t_ha, 2),
        item=request.item,
        area=request.area,
        confidence=confidence,
        feature_importance=feature_importance
    )
