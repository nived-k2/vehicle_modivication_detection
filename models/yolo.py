from ultralytics import YOLO
import cv2

# Mapping class IDs to part names
CLASS_ID_TO_PART = {
    0: "exhaust",
    1: "headlight"
}

# Expand bounding box size
EXPAND_RATIO = 0.15

class YOLOModel:
    def __init__(self, model_path):
        self.model = YOLO(model_path)  # Load the YOLO model

    def detect(self, image_path, conf_threshold=0.2):  # Adjust confidence threshold
        results = self.model(image_path)  # Run detection
        detections = []

        # ✅ Load image size using OpenCV
        image = cv2.imread(image_path)
        image_height, image_width = image.shape[:2]

        for result in results:
            if not hasattr(result, 'boxes') or result.boxes is None:
                continue  # Skip if no boxes detected

            for box in result.boxes:
                conf = box.conf.item()
                class_id = int(box.cls.item())

                if conf >= conf_threshold:
                    x1, y1, x2, y2 = box.xyxy.tolist()[0]

                    # ✅ Expand bounding box before cropping
                    width = x2 - x1
                    height = y2 - y1
                    x1 -= width * EXPAND_RATIO
                    x2 += width * EXPAND_RATIO
                    y1 -= height * EXPAND_RATIO
                    y2 += height * EXPAND_RATIO

                    # Ensure bounding box remains within image bounds
                    x1, y1, x2, y2 = max(0, x1), max(0, y1), min(x2, image_width), min(y2, image_height)

                    part_name = CLASS_ID_TO_PART.get(class_id, "unknown")
                    print(f"[DEBUG] Class ID: {class_id}, Mapped Part: {part_name}, Expanded Bounding Box: {x1, y1, x2, y2}")

                    detections.append({
                        "bbox": [x1, y1, x2, y2],
                        "part": part_name,
                        "confidence": conf
                    })

        return detections
