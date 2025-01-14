from modules.detection import ObjectDetection
from modules.anomaly_detection import AnomalyDetector
from modules.preprocessing import preprocess_image
from modules.result_display import display_results
from PIL import Image
import os
import json

def main(image_path, brand, model, part):
    # Paths for YOLO dataset and models
    yolo_dataset_path = f"C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection - Copy/data/yolo/{brand}/{model}/{part}"
    yolo_model_path = f"C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection - Copy/models/{brand}_{model}_{part}_yolo.pt"
    autoencoder_model_path = f"C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection - Copy/models/{brand}_{model}_{part}_autoencoder.pth"

    print(f"Using YOLO dataset path: {yolo_dataset_path}")
    print(f"Using YOLO model path: {yolo_model_path}")
    print(f"Using Autoencoder model path: {autoencoder_model_path}")

    # Validate file paths
    if not os.path.exists(yolo_model_path):
        return {"status": f"YOLO model not found for {brand} {model} {part}"}
    if not os.path.exists(autoencoder_model_path):
        return {"status": f"Autoencoder model not found for {brand} {model} {part}"}
    if not os.path.exists(image_path):
        return {"status": "Input image not found"}

    # Load YOLO model
    print("Loading YOLO model...")
    yolo_model = ObjectDetection(yolo_model_path)
    detections = yolo_model.detect(image_path)
    print("Detections:", detections)

    if not detections:
        print("No objects detected by YOLO.")
        print("May have a chance of modification.")
        return {"status": "Modification Detected."}

    # Load Autoencoder model
    print("Loading Autoencoder model...")
    anomaly_detector = AnomalyDetector(autoencoder_model_path)

    # Use the cropped image for anomaly detection
    cropped_image_path = "C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection/data/autoencoder/crop/test/cropped_image.jpg"
    if not os.path.exists(cropped_image_path):
        print(f"Error: Cropped image not found at {cropped_image_path}")
        return {"Error": f"Cropped image not found at {cropped_image_path}"}

    print("Loading cropped image...")
    cropped_image = Image.open(cropped_image_path).convert("L")
    preprocessed_image = preprocess_image(cropped_image).unsqueeze(0)
    print("Preprocessed image shape:", preprocessed_image.shape)

    # Perform anomaly detection
    print("Performing anomaly detection...")
    reconstruction_error = anomaly_detector.compute_reconstruction_error(preprocessed_image)
    print("Reconstruction Error:", reconstruction_error)

    # Dynamic threshold computation
    # Load error statistics from config directory
    with open("C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection - Copy/config/error_statistics.json", "r") as f:
        error_statistics = json.load(f)

    if brand in error_statistics and model in error_statistics[brand] and part in error_statistics[brand][model]:
        mean_error = error_statistics[brand][model][part]["mean_error"]
        std_error = error_statistics[brand][model][part]["std_error"]
    else:
        return {"status": f"Error statistics not found for {brand} {model} {part}"}


    alpha = 2.0        # Multiplier for standard deviation
    threshold = mean_error + (alpha * std_error)
    print(f"Dynamic Threshold: {threshold}")

    classification = anomaly_detector.classify_anomaly(reconstruction_error, threshold)
    print("Classification:", classification)

    return {f"{brand} {model} {part}": classification}

