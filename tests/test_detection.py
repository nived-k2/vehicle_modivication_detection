import unittest
from modules.detection import ObjectDetection

class TestDetection(unittest.TestCase):
    def setUp(self):
        self.detector = ObjectDetection(model_path="models/yolo.pt")

    def test_detect_parts(self):
        result = self.detector.detect_parts("test_images/test_image.jpg")
        self.assertIsNotNone(result)
        self.assertTrue(len(result) > 0)

if __name__ == "__main__":
    unittest.main()
