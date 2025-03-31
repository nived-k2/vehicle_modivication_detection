from modules.detection import ObjectDetection
from modules.anomaly_detection import AnomalyDetector
from models.yolo import YOLOModel
from app.manual_cropping import crop_image
from modules.preprocessing import preprocess_image
from modules.result_display import display_results, append_modification
from PIL import Image
import os
import json

def main(image_path, brand, model, detected_part):
    print(f"\n--- Starting Detection for {brand} {model} {detected_part} ---")

    # Load Part Detection YOLO Model
    part_detection_model = YOLOModel("C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection - Copy/models/best (2).pt")
    detections = part_detection_model.detect(image_path)

    if not detections:
        print("[ERROR] No part detected. Please upload a clearer image.")
        return {"status": "No part detected. Please upload a clearer image."}

    bbox = detections[0]['bbox']

    # ✅ Crop detected part using expanded bounding box
    cropped_image_path = "C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection - Copy/croped/croped_image.jpg"
    crop_image(image_path, bbox, cropped_image_path)

    # ✅ Debug: Check Cropped Image Size
    cropped_image = Image.open(cropped_image_path)
    print(f"[DEBUG] Cropped Image Size: {cropped_image.size}")

    # ✅ Resize Cropped Image to YOLO Expected Size
    cropped_image.save(cropped_image_path)

    print(f"[INFO] Cropped image saved at: {cropped_image_path}")

    # Paths for YOLO and Autoencoder Models
    yolo_model_path = f"C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection - Copy/models/{brand}_{model}_{detected_part}_yolo.pt"
    autoencoder_model_path = f"C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection - Copy/models/{brand}_{model}_{detected_part}_autoencoder.pth"

    print(f"[INFO] Using YOLO Model Path: {yolo_model_path}")
    print(f"[INFO] Using Autoencoder Model Path: {autoencoder_model_path}")

    if not os.path.exists(yolo_model_path):
        print(f"[ERROR] YOLO model not found for {brand} {model} {detected_part}")
        return {"status": f"YOLO model not found for {brand} {model} {detected_part}"}

    if not os.path.exists(autoencoder_model_path):
        print(f"[ERROR] Autoencoder model not found for {brand} {model} {detected_part}")
        return {"status": f"Autoencoder model not found for {brand} {model} {detected_part}"}

    # Load Brand-Model-Specific YOLO Model
    print(f"\n[INFO] Loading YOLO Model for {brand} {model} {detected_part}...")
    yolo_model = ObjectDetection(yolo_model_path)
    print("[DEBUG] Running second YOLO detection on cropped image...")
    part_detections = yolo_model.detect(cropped_image_path)
    print(f"[DEBUG] Second YOLO Detection Results: {part_detections}")

    if not part_detections:
        print("[INFO] Modification Detected: No object found in cropped image.")
        append_modification(brand, model, detected_part, "Modified", cropped_image_path)  # ✅ Added PDF logging
        return {"status": "Modification Detected."}

    # Load Autoencoder Model
    print(f"\n[INFO] Loading Autoencoder Model for {brand} {model} {detected_part}...")
    anomaly_detector = AnomalyDetector(autoencoder_model_path)
    cropped_image = Image.open(cropped_image_path).convert("L")
    preprocessed_image = preprocess_image(cropped_image).unsqueeze(0)

    # Compute Reconstruction Error
    reconstruction_error = anomaly_detector.compute_reconstruction_error(preprocessed_image)
    print(f"[INFO] Reconstruction Error: {reconstruction_error}")

    # Load error statistics
    with open("C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection - Copy/config/error_statistics.json", "r") as f:
        error_statistics = json.load(f)

    if brand in error_statistics and model in error_statistics[brand] and detected_part in error_statistics[brand][model]:
        mean_error = error_statistics[brand][model][detected_part]["mean_error"]
        std_error = error_statistics[brand][model][detected_part]["std_error"]
    else:
        print(f"[ERROR] Error statistics not found for {brand} {model} {detected_part}")
        return {"status": f"Error statistics not found for {brand} {model} {detected_part}"}

    # Compute Dynamic Threshold
    threshold = mean_error + (2 * std_error)
    print(f"[INFO] Dynamic Threshold: {threshold}")

    # Classify Anomaly
    classification = anomaly_detector.classify_anomaly(reconstruction_error, threshold)
    print(f"[RESULT] Final Classification: {classification}")

    if classification == "Modified":
        append_modification(brand, model, detected_part, "Modified", cropped_image_path)  # ✅ Added PDF logging

    return {f"{brand} {model} {detected_part}": classification}
