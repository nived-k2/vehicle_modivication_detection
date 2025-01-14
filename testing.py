from modules.detection import ObjectDetection
from modules.anomaly_detection import AnomalyDetector
from modules.preprocessing import preprocess_image
from modules.result_display import display_results
from PIL import Image
import os


def main():
    vehicle = "dominar"
    part = "headlight"

    yolo_model_path = f"C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection/models/{vehicle}_{part}_yolo.pt"
    autoencoder_model_path = f"C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection/models/{vehicle}_{part}_autoencoder.pth"
    test_image_path = "C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection/data/autoencoder/headlight/train/WhatsApp Image 2024-12-21 at 4.59.42 PM.jpeg"

    # Debug print statements to ensure file paths are correct
    print(f"Using YOLO model path: {yolo_model_path}")
    print(f"Using Autoencoder model path: {autoencoder_model_path}")
    print(f"Using test image path: {test_image_path}")

    # Check if files exist
    if not os.path.exists(yolo_model_path):
        print(f"Error: YOLO model not found at {yolo_model_path}")
        return
    if not os.path.exists(autoencoder_model_path):
        print(f"Error: Autoencoder model not found at {autoencoder_model_path}")
        return
    if not os.path.exists(test_image_path):
        print(f"Error: Test image not found at {test_image_path}")
        return

    # Load YOLO model and detect objects
    print("Loading YOLO model...")
    yolo_model = ObjectDetection(yolo_model_path)
    detections = yolo_model.detect(test_image_path)
    print("Detections:", detections)

    # Check if YOLO detected anything
    if not detections:
        print("No objects detected by YOLO.")
        return

    # Load Autoencoder and perform anomaly detection
    print("Loading Autoencoder model...")
    anomaly_detector = AnomalyDetector(autoencoder_model_path)

    # Simulate a cropped image
    cropped_image_path = "C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection/data/autoencoder/headlight/test/cropped_image.jpg"
    if not os.path.exists(cropped_image_path):
        print(f"Error: Cropped image not found at {cropped_image_path}")
        return

    print("Loading cropped image...")
    cropped_image = Image.open(cropped_image_path).convert("L")
    preprocessed_image = preprocess_image(cropped_image).unsqueeze(0)
    print("Preprocessed image shape:", preprocessed_image.shape)

    # Compute reconstruction error and classify anomaly
    print("Performing anomaly detection...")
    reconstruction_error = anomaly_detector.compute_reconstruction_error(preprocessed_image)
    print("Reconstruction Error:", reconstruction_error)

    classification = anomaly_detector.classify_anomaly(reconstruction_error, threshold=0.25)
    print("Classification:", classification)

    # Display results
    results = {f"{vehicle} {part}": classification}
    display_results(results)


if __name__ == "__main__":
    main()
