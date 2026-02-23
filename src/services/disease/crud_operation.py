import cv2
import numpy as np
from fastapi import HTTPException
import uuid
from src.core.database import supabase

def save_gradcam_image_to_supabase(original_image, heatmap):
    # Resize heatmap to image size
    heatmap = cv2.resize(
        heatmap,
        (original_image.shape[1], original_image.shape[0])
    )

    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    overlay = cv2.addWeighted(original_image, 0.6, heatmap, 0.4, 0)

    # Encode image to PNG (in memory)
    success, encoded_image = cv2.imencode(".png", overlay)
    if not success:
        raise HTTPException(status_code=500, detail="Image encoding failed")

    image_bytes = encoded_image.tobytes()
    file_name = f"gradcam_{uuid.uuid4().hex}.png"

    # Upload directly to Supabase Storage
    response = supabase.storage.from_("crop_disease").upload(
        path=file_name,
        file=image_bytes,
        file_options={"content-type": "image/png"}
    )

        # ✅ correct error check
    # if response.error:
    #     raise HTTPException(status_code=400, detail=str(response.error))

    # Get public URL
    public_url = supabase.storage.from_("crop_disease").get_public_url(file_name)

    return public_url


def save_prediction_to_db(
    user_id: str,
    label: str,
    confidence: float,
    heatmap_path: str
):
    try:
        response = (
            supabase
            .table("crop_disease_predictions")
            .insert({
                "user_id": user_id,
                "label": label,
                "confidence": confidence,
                "heatmap_path": heatmap_path,
            })
            .execute()
        )

    except Exception as e:
        # ⬇️ throw a DIFFERENT exception
        raise Exception(
            f"Failed to insert disease prediction for user {user_id}"
        ) from e