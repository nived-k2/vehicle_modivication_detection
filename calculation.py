import os
import torch
from PIL import Image
from modules.anomaly_detection import AnomalyDetector
from modules.preprocessing import preprocess_image

def compute_error_statistics(autoencoder_model_path, stock_images_folder):
    """
    Compute mean and standard deviation of reconstruction errors for stock images.

    Args:
        autoencoder_model_path (str): Path to the trained autoencoder model.
        stock_images_folder (str): Path to the folder containing stock images.

    Returns:
        tuple: (mean_error, std_error)
    """
    anomaly_detector = AnomalyDetector(autoencoder_model_path)
    reconstruction_errors = []

    for image_name in os.listdir(stock_images_folder):
        image_path = os.path.join(stock_images_folder, image_name)
        if image_path.lower().endswith(('jpg', 'png', 'jpeg')):
            image = Image.open(image_path).convert("L")  # Convert to grayscale
            preprocessed_image = preprocess_image(image).unsqueeze(0)  # Preprocess and add batch dimension
            error = anomaly_detector.compute_reconstruction_error(preprocessed_image)
            reconstruction_errors.append(error)

    reconstruction_errors_tensor = torch.tensor(reconstruction_errors)
    mean_error = torch.mean(reconstruction_errors_tensor).item()
    std_error = torch.std(reconstruction_errors_tensor).item()

    return mean_error, std_error

# Example Usage
autoencoder_model_path = "C:/Users/HP/OneDrive\Desktop/vehicle_modivication_detection/models/tvs_raider_exhaust_autoencoder.pth"
stock_images_folder = "C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection/data/autoencoder/tvs/raider/exhaust/train"
mean_error, std_error = compute_error_statistics(autoencoder_model_path, stock_images_folder)
print(f"Mean Error: {mean_error}, Std Error: {std_error}")
