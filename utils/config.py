import os

YOLO_DATA_PATH = os.path.join("data", "yolo")
AUTOENCODER_DATA_PATH = os.path.join("data", "autoencoder")
YOLO_CONFIDENCE_THRESHOLD = 0.5
AUTOENCODER_THRESHOLD = 0.05
IMAGE_SIZE = (64, 64)
PREDEFINED_CROPPING = {
    "headlight": [100, 50, 200, 200],
    "exhaust": [300, 100, 400, 250],
    "saree_guard": [150, 200, 250, 350]
}
