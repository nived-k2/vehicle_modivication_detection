from models.yolo import YOLOModel

class ObjectDetection:
    def __init__(self, model_path):
        """
        Initializes the ObjectDetection class with a YOLO model.
        Args:
            model_path (str): Path to the trained YOLO model file.
        """
        self.model = YOLOModel(model_path)  # Initialize YOLO model

    def detect(self, image_path, conf_threshold=0.7):
        """
        Detect objects in the given image.
        Args:
            image_path (str): Path to the input image.
            conf_threshold (float): Confidence threshold for detections.
        Returns:
            list: List of detections with bounding boxes, classes, and confidence.
        """
        return self.model.detect(image_path, conf_threshold)
