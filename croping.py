import cv2
import torch
import os
import numpy as np
from ultralytics import YOLO


def expand_bbox(bbox, img_width, img_height, expansion_factor=0.1):
    """
    Expands the bounding box by a given factor while ensuring it remains within image bounds.
    """
    x_min, y_min, x_max, y_max = bbox
    width = x_max - x_min
    height = y_max - y_min

    # Expand box
    x_min = max(0, int(x_min - expansion_factor * width))
    y_min = max(0, int(y_min - expansion_factor * height))
    x_max = min(img_width, int(x_max + expansion_factor * width))
    y_max = min(img_height, int(y_max + expansion_factor * height))

    return x_min, y_min, x_max, y_max


def detect_and_crop(model_path, image_folder, output_folder, expansion_factor=0.1, conf_threshold=0.3):
    """
    Detects objects using YOLOv8, expands bounding boxes, and saves cropped images.
    """
    # Load YOLOv8 model
    model = YOLO(model_path)

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Process images
    for img_name in os.listdir(image_folder):
        img_path = os.path.join(image_folder, img_name)
        img = cv2.imread(img_path)
        if img is None:
            continue

        img_height, img_width, _ = img.shape

        # Perform detection
        results = model(img)[0]

        for i, box in enumerate(results.boxes):
            if box.conf[0] < conf_threshold:
                continue  # Skip detections below confidence threshold

            x_min, y_min, x_max, y_max = box.xyxy[0].cpu().numpy()
            x_min, y_min, x_max, y_max = expand_bbox((x_min, y_min, x_max, y_max), img_width, img_height,
                                                     expansion_factor)

            # Crop the detected object
            cropped_img = img[y_min:y_max, x_min:x_max]

            # Save cropped image
            save_path = os.path.join(output_folder, f"{os.path.splitext(img_name)[0]}_crop_{i}.jpg")
            cv2.imwrite(save_path, cropped_img)
            print(f"Saved cropped image: {save_path}")


if __name__ == "__main__":
    model_path = "C:/Users/HP/OneDrive\Desktop/vehicle_modivication_detection - Copy/models/tvs_raider_headlight_yolo.pt"  # Update with your model path
    image_folder = "C:/Users/HP/OneDrive/Desktop/tr"  # Update with your input image folder
    output_folder = "C:/Users/HP/OneDrive/Desktop/tvscrop"  # Update with your desired output folder

    detect_and_crop(model_path, image_folder, output_folder, expansion_factor=0.1)
