"""Model and encoder loading for fertilizer recommendation.

This module handles lazy loading and caching of the fertilizer prediction model
and label encoders.
"""

import pickle
from src.core.config import settings

# Global caches for model and encoders
_model = None
_fertilizer_encoder = None
_crop_encoder = None
_soil_encoder = None


def get_fertilizer_model():
    """
    Load and cache the fertilizer prediction model.
    Uses lazy loading pattern - model is loaded only once on first request.

    Returns:
        Trained fertilizer prediction model
    """
    global _model

    if _model is None:
        with open(settings.fertilizer_model_path, 'rb') as f:
            _model = pickle.load(f)
        print(f"✅ Fertilizer model loaded from {settings.fertilizer_model_path}")

    return _model


def get_fertilizer_encoder():
    """
    Load and cache the fertilizer label encoder.
    This encoder converts fertilizer names to numerical labels and vice versa.

    Returns:
        Label encoder for fertilizer names
    """
    global _fertilizer_encoder

    if _fertilizer_encoder is None:
        with open(settings.fertilizer_encoder_path, 'rb') as f:
            _fertilizer_encoder = pickle.load(f)
        print(f"✅ Fertilizer encoder loaded from {settings.fertilizer_encoder_path}")

    return _fertilizer_encoder


def get_crop_encoder():
    """
    Load and cache the crop label encoder.
    This encoder converts crop names to numerical labels.

    Returns:
        Label encoder for crop names
    """
    global _crop_encoder

    if _crop_encoder is None:
        with open(settings.crop_encoder_path, 'rb') as f:
            _crop_encoder = pickle.load(f)
        print(f"✅ Crop encoder loaded from {settings.crop_encoder_path}")

    return _crop_encoder


def get_soil_encoder():
    """
    Load and cache the soil color label encoder.
    This encoder converts soil color names to numerical labels.

    Returns:
        Label encoder for soil colors
    """
    global _soil_encoder

    if _soil_encoder is None:
        with open(settings.soil_encoder_path, 'rb') as f:
            _soil_encoder = pickle.load(f)
        print(f"✅ Soil encoder loaded from {settings.soil_encoder_path}")

    return _soil_encoder
