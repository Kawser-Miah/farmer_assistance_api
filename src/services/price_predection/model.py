"""Model and bundle loading for price prediction.

This module handles lazy loading and caching of the price prediction bundle
which contains the model, label encoders, and feature names.
"""

import pickle
from src.core.config import settings

# Global cache for price prediction bundle
_bundle = None


def get_price_prediction_bundle():
    """
    Load and cache the price prediction bundle.
    Uses lazy loading pattern - bundle is loaded only once on first request.
    
    The bundle contains:
        - 'model': Trained price prediction model (sklearn)
        - 'label_encoders': Dict of label encoders for categorical features
        - 'features': List of feature names in correct order

    Returns:
        Dictionary containing model, label_encoders, and features

    Raises:
        FileNotFoundError: If bundle file not found
        pickle.UnpicklingError: If bundle file is corrupted
    """
    global _bundle

    if _bundle is None:
        with open(settings.price_predection_bundle_path, 'rb') as f:
            _bundle = pickle.load(f)
        print(f"✅ Price prediction bundle loaded from {settings.price_predection_bundle_path}")

    return _bundle
