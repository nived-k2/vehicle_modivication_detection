import os
import torch
from PIL import Image, ImageOps
from models.autoencoder import DeepAutoencoder
from torchvision import transforms

def resize_with_padding(image, target_size=(64, 64)):
    """
    Resize the image while maintaining its aspect ratio and pad to the target size.
    """
    image.thumbnail(target_size, Image.Resampling.LANCZOS)
    delta_w = target_size[0] - image.size[0]
    delta_h = target_size[1] - image.size[1]
    padding = (delta_w // 2, delta_h // 2, delta_w - (delta_w // 2), delta_h - (delta_h // 2))
    padded_image = ImageOps.expand(image, padding, fill="black")
    return padded_image

def load_weights_ignore_mismatch(model, checkpoint_path):
    """
    Load weights into the model, ignoring mismatched layers.

    Args:
        model (nn.Module): The model to load weights into.
        checkpoint_path (str): Path to the checkpoint file.
    """
    checkpoint = torch.load(checkpoint_path, map_location="cpu")
    model_state_dict = model.state_dict()

    # Compare shapes in the checkpoint and the model
    for key in checkpoint.keys():
        if key in model_state_dict:
            print(f"{key}: Checkpoint shape: {checkpoint[key].shape}, Model shape: {model_state_dict[key].shape}")
        else:
            print(f"{key}: Not found in model state dict.")

    # Filter out mismatched keys
    matched_layers = 0
    for key, value in checkpoint.items():
        if key in model_state_dict and model_state_dict[key].size() == value.size():
            model_state_dict[key] = value
            matched_layers += 1

    model.load_state_dict(model_state_dict)
    print(f"Loaded {matched_layers}/{len(checkpoint)} matching layers.")

def compute_error_statistics(autoencoder_model_path, stock_images_folder):
    """
    Compute mean and standard deviation of reconstruction errors for stock images.

    Args:
        autoencoder_model_path (str): Path to the trained DeepAutoencoder model.
        stock_images_folder (str): Path to the folder containing stock images.

    Returns:
        tuple: (mean_error, std_error)
    """
    # Initialize the DeepAutoencoder model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = DeepAutoencoder()
    load_weights_ignore_mismatch(model, autoencoder_model_path)  # Ignore mismatched layers
    model.to(device)
    model.eval()

    reconstruction_errors = []

    # Define preprocessing pipeline
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])

    # Process each image in the stock folder
    for image_name in os.listdir(stock_images_folder):
        image_path = os.path.join(stock_images_folder, image_name)
        if image_path.lower().endswith(('jpg', 'png', 'jpeg')):
            # Load, resize with padding, and preprocess the image
            image = Image.open(image_path).convert("L")  # Convert to grayscale
            image = resize_with_padding(image, target_size=(64, 64))  # Resize with padding
            preprocessed_image = transform(image).unsqueeze(0).to(device)  # Add batch dimension

            # Compute reconstruction and error
            with torch.no_grad():
                reconstructed_image = model(preprocessed_image)
                error = torch.mean((preprocessed_image - reconstructed_image) ** 2).item()
                reconstruction_errors.append(error)

    # Calculate mean and standard deviation
    reconstruction_errors_tensor = torch.tensor(reconstruction_errors)
    mean_error = torch.mean(reconstruction_errors_tensor).item()
    std_error = torch.std(reconstruction_errors_tensor).item()

    return mean_error, std_error

# Example Usage
if __name__ == "__main__":
    autoencoder_model_path = "C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection - Copy/models/bajaj_dominar_headlight_autoencoder.pth"
    stock_images_folder = "C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection - Copy/data/autoencoder/bajaj/dominar/headlight/train"

    mean_error, std_error = compute_error_statistics(autoencoder_model_path, stock_images_folder)
    print(f"Mean Reconstruction Error: {mean_error:.6f}")
    print(f"Standard Deviation of Reconstruction Error: {std_error:.6f}")
