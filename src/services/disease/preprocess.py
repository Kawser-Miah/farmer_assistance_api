import cv2
import numpy as np
from tensorflow.keras.applications.resnet50 import preprocess_input # type: ignore
import tensorflow as tf

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


def make_gradcam_heatmap(image, model, last_conv_layer_name):
    image = tf.convert_to_tensor(image)

    last_conv_layer = model.get_layer(last_conv_layer_name)

    grad_model = tf.keras.models.Model(
        inputs=model.inputs,
        outputs=[last_conv_layer.output, model.outputs[0]],
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(image)

        if isinstance(predictions, (list, tuple)):
            predictions = predictions[0]

        class_idx = tf.argmax(predictions[0])
        loss = predictions[:, class_idx]

    grads = tape.gradient(loss, conv_outputs)

    if isinstance(grads, (list, tuple)):
        grads = grads[0]

    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    conv_outputs = conv_outputs[0]
    heatmap = tf.reduce_sum(conv_outputs * pooled_grads, axis=-1)

    heatmap = tf.maximum(heatmap, 0)
    heatmap /= tf.reduce_max(heatmap) + 1e-8

    return heatmap.numpy()

def overlay_gradcam(original_image, heatmap, alpha=0.4):
    heatmap = cv2.resize(heatmap, (original_image.shape[1], original_image.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    return cv2.addWeighted(original_image, 1 - alpha, heatmap, alpha, 0)


# GRADCAM_DIR = "media/gradcam"

# def save_gradcam_image(original_image, heatmap):
#     os.makedirs(GRADCAM_DIR, exist_ok=True)

#     # Resize heatmap to image size
#     heatmap = cv2.resize(
#         heatmap,
#         (original_image.shape[1], original_image.shape[0])
#     )

#     heatmap = np.uint8(255 * heatmap)
#     heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

#     overlay = cv2.addWeighted(original_image, 0.6, heatmap, 0.4, 0)

#     filename = f"gradcam_{uuid.uuid4().hex}.png"
#     filepath = os.path.join(GRADCAM_DIR, filename)

#     cv2.imwrite(filepath, overlay)

#     return filepath

