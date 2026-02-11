import tensorflow as tf
import json
from src.core.config import settings

_model = None

def get_model():

    global _model

    if _model is None:
        _model = tf.keras.models.load_model(settings.crop_disease_detection_model_path)
        print(f"Disease model loaded from {settings.crop_disease_detection_model_path}")

    return _model
    


def get_class_names():
    with open(settings.crop_disease_detection_class_names_path, "r") as f:
        class_names = json.load(f)

    print(f"Class names loaded from {settings.crop_disease_detection_class_names_path}")
    return class_names


# get_model()  # Preload model at startup