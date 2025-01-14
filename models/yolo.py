from ultralytics import YOLO

class YOLOModel:
    def __init__(self, model_path):
        """
        Initializes the YOLO model for object detection.
        Args:
            model_path (str): Path to the YOLO model file.
        """
        self.model = YOLO(model_path)  # Load the YOLO model

    def detect(self, image_path, conf_threshold=0.7):
        results = self.model(image_path)  # Run detection
        print("Raw YOLO results:", results)  # Debug: Print raw results
        detections = []
        for result in results:
            for box in result.boxes:
                conf = box.conf.item()
                if conf >= conf_threshold:
                    detections.append({
                        "bbox": box.xyxy.tolist()[0],  # Bounding box coordinates
                        "class_id": int(box.cls.item()),  # Class ID
                        "confidence": conf  # Confidence score
                    })
        return detections
