"""Model and encoder loading for yield estimation.

This module handles lazy loading and caching of the yield prediction model
and label encoders.
"""
import joblib
import pickle
from src.core.config import settings

# Global caches for model and encoders
_model = None
_item_encoder = None
_area_encoder = None


def get_yield_model():
    """
    Load and cache the yield prediction model.
    Uses lazy loading pattern - model is loaded only once on first request.

    Returns:
        Trained yield prediction model
    """
    global _model

    if _model is None:
       
        _model = joblib.load(settings.yield_model_path)
        print(f"✅ Yield model loaded from {settings.yield_model_path}")

    return _model


def get_item_encoder():
    """
    Load and cache the item (crop) label encoder.
    This encoder converts crop names to numerical labels.

    Returns:
        Label encoder for crop/item names
    """
    global _item_encoder

    if _item_encoder is None:
        
        _item_encoder = joblib.load(settings.item_encoder_path)
        print(f"✅ Item encoder loaded from {settings.item_encoder_path}")

    return _item_encoder


def get_area_encoder():
    """
    Load and cache the area (country/region) label encoder.
    This encoder converts area names to numerical labels.

    Returns:
        Label encoder for area names
    """
    global _area_encoder

    if _area_encoder is None:
        _area_encoder = joblib.load(settings.area_encoder_path)
        print(f"✅ Area encoder loaded from {settings.area_encoder_path}")

    return _area_encoder
