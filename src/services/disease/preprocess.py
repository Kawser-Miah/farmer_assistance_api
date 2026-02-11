import cv2
import numpy as np
from tensorflow.keras.applications.resnet50 import preprocess_input

DEFAULT_IMAGE_SIZE = (224, 224)

def preprocess_image(image_bytes: bytes):
    # bytes → numpy array
    np_arr = np.frombuffer(image_bytes, np.uint8)

    # decode image (BGR)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Invalid image")

    # resize
    image = cv2.resize(image, DEFAULT_IMAGE_SIZE)

    # BGR → RGB (IMPORTANT)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # float32
    image = image.astype("float32")

    # ResNet50 preprocessing (CRITICAL)
    image = preprocess_input(image)

    # add batch dimension
    image = np.expand_dims(image, axis=0)

    return image
