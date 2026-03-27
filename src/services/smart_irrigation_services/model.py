import joblib
from src.core.config import settings

_model = None
_soil_encoder = None
_crop_encoder = None
_stage_encoder = None


def get_irrigation_model():
    """
    Load and cache the smart irrigation model.
    Uses lazy loading pattern - model is loaded only once on first request.
    """
    global _model

    if _model is None:
        _model = joblib.load(settings.smart_irrigation_model_path)
        print(f"Smart irrigation model loaded from {settings.smart_irrigation_model_path}")

    return _model

def get_irrigation_soil_encoder():
    """
    Load and cache the smart irrigation soil encoder.
    Uses lazy loading pattern - encoder is loaded only once on first request.
    """
    global _soil_encoder

    if _soil_encoder is None:
        _soil_encoder = joblib.load(settings.irrigation_soil_encoder_path)
        print(f"Smart irrigation soil encoder loaded from {settings.irrigation_soil_encoder_path}")

    return _soil_encoder

def get_irrigation_crop_encoder():
    """
    Load and cache the smart irrigation crop encoder.
    Uses lazy loading pattern - encoder is loaded only once on first request.
    """
    global _crop_encoder

    if _crop_encoder is None:
        _crop_encoder = joblib.load(settings.irrigation_crop_encoder_path)
        print(f"Smart irrigation crop encoder loaded from {settings.irrigation_crop_encoder_path}")

    return _crop_encoder

def get_irrigation_stage_encoder():
    """
    Load and cache the smart irrigation stage encoder.
    Uses lazy loading pattern - encoder is loaded only once on first request.
    """
    global _stage_encoder

    if _stage_encoder is None:
        _stage_encoder = joblib.load(settings.irrigation_stage_encoder_path)
        print(f"Smart irrigation stage encoder loaded from {settings.irrigation_stage_encoder_path}")

    return _stage_encoder


