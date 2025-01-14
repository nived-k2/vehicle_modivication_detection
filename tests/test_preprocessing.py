import unittest
from modules.preprocessing import preprocess_image
from PIL import Image

class TestPreprocessing(unittest.TestCase):
    def test_preprocess_image(self):
        image = Image.new("RGB", (128, 128))
        transformed = preprocess_image(image)
        self.assertEqual(transformed.shape, (1, 64, 64))

if __name__ == "__main__":
    unittest.main()
