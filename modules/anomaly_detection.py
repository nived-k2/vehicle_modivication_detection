import torch
from models.autoencoder import DeepAutoencoder
import torch.nn as nn

class AnomalyDetector:
    def __init__(self, model_path):
        """
        Initialize the anomaly detector with a trained autoencoder model.
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = DeepAutoencoder()
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()

    def compute_reconstruction_error(self, image):
        """
        Computes the reconstruction error for a given image.
        """
        with torch.no_grad():
            image = image.to(self.device)
            reconstructed = self.model(image)
            mse_loss = nn.MSELoss()
            return mse_loss(reconstructed, image).item()

    def classify_anomaly(self, error, threshold):
        """
        Classifies the part as Modified or Not Modified based on the reconstruction error.
        """
        return "Modified" if error > threshold else "Not Modified"
