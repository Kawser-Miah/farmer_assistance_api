import joblib
from src.core.config import settings

_model = None


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
