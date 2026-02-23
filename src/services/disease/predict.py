import numpy as np
import cv2
from src.services.disease.model import get_model, get_class_names
from src.services.disease.preprocess import preprocess_image, make_gradcam_heatmap
from src.services.disease.crud_operation import save_gradcam_image_to_supabase, save_prediction_to_db

from src.schemas.crop_disease_schemas import DiseasePredictionResponse

def predict_disease(image_bytes: bytes, user_id: str) -> DiseasePredictionResponse:
    if not image_bytes:
        raise ValueError("Empty image input")

    model = get_model()
    class_names = get_class_names()

    image = preprocess_image(image_bytes)

    preds = model.predict(image)
    class_idx = int(np.argmax(preds, axis=1)[0])
    confidence = float(preds[0][class_idx]) * 100
     # 🔹 Decode original image for Grad-CAM overlay
    np_arr = np.frombuffer(image_bytes, np.uint8)
    original_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    
    heatmap = make_gradcam_heatmap(image, model, "conv5_block3_out")  
    path = save_gradcam_image_to_supabase(original_image, heatmap)

    save_prediction_to_db(
        user_id=user_id,
        label=class_names[class_idx],
        confidence=round(confidence, 2),
        heatmap_path=path
    )

    return DiseasePredictionResponse(
        label=class_names[class_idx],
        confidence=round(confidence, 2),
        heatmap_url=path
    )
