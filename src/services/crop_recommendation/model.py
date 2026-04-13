"""Model and encoder loading for crop recommendation.

This module handles lazy loading and caching of the crop recommendation model.
"""

import joblib
from src.core.config import settings

_model = None


def get_crop_recommendation_model():
    """
    Load and cache the crop recommendation model.
    Uses lazy loading pattern - model is loaded only once on first request.

    Returns:
        Trained crop recommendation model
    """
    global _model

    if _model is None:
        _model = joblib.load(settings.crop_recommendation_model_path)
        print(f"✅ Crop recommendation model loaded from {settings.crop_recommendation_model_path}")

    return _model
