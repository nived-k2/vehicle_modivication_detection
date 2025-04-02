from ultralytics import YOLO
import cv2
import numpy as np

# Load YOLO Model
model = YOLO("C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection - Copy/models/tvs_raider_headlight_yolo.pt")

# Load Image
image_path = "C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection - Copy/croped/croped_image.jpg"
image = cv2.imread(image_path)

# Run YOLO Detection
results = model(image_path)

# Extract Bounding Boxes
detections = []
for result in results:
    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy.tolist()[0])  # Bounding box coordinates
        conf = box.conf.item()  # Confidence Score
        class_id = int(box.cls.item())  # Class ID

        detections.append((x1, y1, x2, y2, conf, class_id))

# If detections exist, draw bounding boxes
if detections:
    for (x1, y1, x2, y2, conf, class_id) in detections:
        label = f"Detected: {model.names[class_id]} ({conf:.2f})"

        # Draw Bounding Box
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Put Label
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
else:
    # If no detections, show "Not Detected" on the image
    cv2.putText(image, "Not Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

# Show the Image
cv2.imshow("YOLO Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
