import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image, ImageOps
from models.autoencoder import DeepAutoencoder

# Function to resize image with padding while maintaining aspect ratio
def resize_with_padding(image, target_size=(64, 64)):
    """
    Resize the image while maintaining its aspect ratio and pad to the target size.
    """
    # Use Resampling.LANCZOS instead of ANTIALIAS
    image.thumbnail(target_size, Image.Resampling.LANCZOS)
    delta_w = target_size[0] - image.size[0]
    delta_h = target_size[1] - image.size[1]
    padding = (delta_w // 2, delta_h // 2, delta_w - (delta_w // 2), delta_h - (delta_h // 2))
    padded_image = ImageOps.expand(image, padding, fill="black")  # Use "black" for padding
    return padded_image

# Custom Dataset for Autoencoder Training
class AutoencoderDataset(Dataset):
    def __init__(self, image_dir, transform=None):
        self.image_dir = image_dir
        self.images = [os.path.join(image_dir, img) for img in os.listdir(image_dir) if img.endswith(('jpg', 'png', 'jpeg'))]
        self.transform = transform

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img_path = self.images[idx]
        image = Image.open(img_path).convert("L")  # Convert to grayscale
        image = resize_with_padding(image, target_size=(64, 64))  # Resize with padding
        if self.transform:
            image = self.transform(image)
        return image

# Train the Autoencoder
def train_autoencoder(train_dir, model_save_path, epochs=20, batch_size=32, learning_rate=0.001):
    transform = transforms.Compose([
        transforms.ToTensor(),  # Convert to tensor
        transforms.Normalize((0.5,), (0.5,))  # Normalize pixel values to [-1, 1]
    ])
    dataset = AutoencoderDataset(image_dir=train_dir, transform=transform)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    model = DeepAutoencoder()
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    print(f"Training on {device}...")
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        for images in dataloader:
            images = images.to(device)
            reconstructed = model(images)
            loss = criterion(reconstructed, images)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        print(f"Epoch [{epoch+1}/{epochs}], Loss: {running_loss/len(dataloader):.4f}")

    torch.save(model.state_dict(), model_save_path)
    print(f"Model saved to {model_save_path}")

if __name__ == "__main__":
    train_autoencoder(
        train_dir="C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection - Copy/data/autoencoder/bajaj/dominar/exhaust/train",
        model_save_path="C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection - Copy/models/bajaj_dominar_exhaust_autoencoder.pth",
        epochs=100,
        batch_size=32,
        learning_rate=0.01
    )
