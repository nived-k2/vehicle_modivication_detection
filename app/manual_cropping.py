import cv2
import os

def crop_image(image_path, bbox, output_path):
    """
    Crops the detected region using bounding box coordinates.
    Args:
        image_path (str): Path to the original image.
        bbox (list): Bounding box coordinates [x_min, y_min, x_max, y_max].
        output_path (str): Path to save the cropped image.
    """
    image = cv2.imread(image_path)
    x_min, y_min, x_max, y_max = map(int, bbox)
    cropped_image = image[y_min:y_max, x_min:x_max]
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, cropped_image)
    print(f"Cropped image saved to {output_path}")
