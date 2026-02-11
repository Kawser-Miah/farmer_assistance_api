import numpy as np
from src.services.disease.model import get_model, get_class_names
from src.services.disease.preprocess import preprocess_image

def predict_disease(image_bytes: bytes):
    if not image_bytes:
        raise ValueError("Empty image input")

    model = get_model()
    class_names = get_class_names()

    image = preprocess_image(image_bytes)

    preds = model.predict(image)
    class_idx = int(np.argmax(preds, axis=1)[0])
    confidence = float(preds[0][class_idx]) * 100

    return {
        "label": class_names[class_idx],
        "confidence": round(confidence, 2)
    }
