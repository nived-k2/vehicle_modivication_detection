import os
import cv2
from ultralytics import YOLO

def preprocess_and_crop(input_dir, output_dir, model_path):
    """
    Preprocess and crop images using YOLOv8 for object detection.

    Args:
        input_dir (str): Path to the input dataset containing original images.
        output_dir (str): Path to save preprocessed cropped images.
        model_path (str): Path to YOLOv8 weights file.

    Returns:
        None
    """
    # Load YOLOv8 model
    model = YOLO(model_path)

    # Create output directory structure
    cropped_headlight_dir = os.path.join(output_dir, 'cropped_headlight2')
    os.makedirs(cropped_headlight_dir, exist_ok=True)

    # Process each image in the input directory
    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        image = cv2.imread(input_path)

        if image is None:
            print(f"Failed to load image: {filename}")
            continue

        # Perform YOLOv8 detection
        results = model(image)

        # Check if any bounding boxes are detected
        if len(results[0].boxes) == 0:
            print(f"No bounding boxes detected for: {filename}")
            continue

        # Iterate through detected bounding boxes
        for i, box in enumerate(results[0].boxes):
            # Extract bounding box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())  # Convert coordinates to integers

            # Crop the image
            cropped_image = image[y1:y2, x1:x2]

            # Save the cropped image
            cropped_filename = f"{os.path.splitext(filename)[0]}cropped{i}.jpg"
            cropped_path = os.path.join(cropped_headlight_dir, cropped_filename)
            cv2.imwrite(cropped_path, cropped_image)

            print(f"Cropped image saved at: {cropped_path}")

# Example usage
if __name__ == "__main__":
    input_dir = "C:/Users/HP/Downloads/WhatsApp Unknown 2024-12-22 at 11.26.59 PM"
    output_dir = "C:/Users/HP/OneDrive/Desktop/croped"
    model_path = "C:/Users/HP/Downloads/best (4).pt"

    preprocess_and_crop(input_dir, output_dir, model_path)