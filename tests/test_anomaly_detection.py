import unittest
import torch
from modules.anomaly_detection import AnomalyDetector

class TestAnomalyDetection(unittest.TestCase):
    def setUp(self):
        # Set up a dummy autoencoder model path for testing
        self.model_path = "C:/Users/HP\OneDrive/Desktop/vehicle_modivication_detection/models/models/{vehicle}_{part}_autoencoder.pth"  # Replace with a valid .pth file path
        self.anomaly_detector = AnomalyDetector(self.model_path)

    def test_compute_reconstruction_error(self):
        # Create dummy tensors for testing
        original = torch.rand(1, 1, 64, 64)  # Example input image tensor
        reconstructed = original.clone()    # Example reconstructed tensor (perfect reconstruction)
        error = self.anomaly_detector.compute_reconstruction_error(original)

        # Assert that reconstruction error is 0 for identical tensors
        self.assertAlmostEqual(error, 0.0, places=5)

    def test_classify_anomaly(self):
        # Test classification logic
        error = 0.05
        threshold = 0.1
        result = self.anomaly_detector.classify_anomaly(error, threshold)
        self.assertEqual(result, "Not Modified")

        error = 0.15
        result = self.anomaly_detector.classify_anomaly(error, threshold)
        self.assertEqual(result, "Modified")

if __name__ == "__main__":
    unittest.main()
