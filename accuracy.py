import os
import torch
from torchvision import transforms
from PIL import Image
from models.autoencoder import DeepAutoencoder
import json

def load_dataset(data_path, transform):
    """
    Loads a dataset from the given path.
    Assumes all images in the folder are of the same category (e.g., Modified).
    """
    dataset = []
    for img_file in os.listdir(data_path):
        if img_file.endswith(('jpg', 'png', 'jpeg')):
            img_path = os.path.join(data_path, img_file)
            img = Image.open(img_path).convert('L')
            dataset.append(transform(img))
    return dataset

def calculate_accuracy(model, dataset, threshold, device):
    """
    Calculates the accuracy of the autoencoder based on reconstruction error.
    Since all images are of the same category, it simply evaluates how many exceed the threshold.
    """
    correct = 0
    total = len(dataset)
    criterion = torch.nn.MSELoss()

    with torch.no_grad():
        for img in dataset:
            img = img.unsqueeze(0).to(device)  # Use device variable
            reconstructed = model(img)
            error = criterion(reconstructed, img).item()
            if error > threshold:
                correct += 1

    accuracy = (correct / total) * 100
    return accuracy

def main():
    # Configuration
    data_path = "C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection - Copy/data/autoencoder/bajaj/dominar/headlight/test"  # Test dataset path
    model_path = "C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection - Copy/models/bajaj_dominar_headlight_autoencoder.pth"  # Model path
    threshold_file = "C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection - Copy/config/error_statistics.json"  # Error statistics path

    # Brand, Model, and Part configuration
    brand = "Bajaj"
    model = "Dominar"
    part = "Headlight"  # Ensure this is a string

    print(f"Brand: {brand}, Model: {model}, Part: {part}")  # Debug: Check values

    # Load model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_instance = DeepAutoencoder()
    model_instance.load_state_dict(torch.load(model_path, map_location=device))
    model_instance.to(device)
    model_instance.eval()

    # Load error statistics
    with open(threshold_file, 'r') as f:
        error_stats = json.load(f)

    print(f"Error Statistics Loaded: {json.dumps(error_stats, indent=2)}")  # Debug: View JSON structure

    # Ensure keys exist in error statistics
    if brand in error_stats and model in error_stats[brand] and part in error_stats[brand][model]:
        mean_error = error_stats[brand][model][part]["mean_error"]
        std_error = error_stats[brand][model][part]["std_error"]
    else:
        available_keys = {b: {m: list(parts.keys()) for m, parts in error_stats[b].items()} for b in error_stats}
        raise KeyError(f"Error statistics not found for {brand} {model} {part}. Available keys: {json.dumps(available_keys, indent=2)}")

    # Calculate dynamic threshold
    alpha = 2  # Standard deviation multiplier
    threshold = mean_error + (alpha * std_error)
    print(f"Dynamic Threshold for {brand} {model} {part}: {threshold}")

    # Preprocessing
    transform = transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])

    # Load dataset
    dataset = load_dataset(data_path, transform)

    # Calculate accuracy
    accuracy = calculate_accuracy(model_instance, dataset, threshold, device)

    print(f"Autoencoder Accuracy: {accuracy:.2f}%")

if __name__ == "__main__":
    main()
