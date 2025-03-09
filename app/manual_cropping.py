import cv2
import os
import time

class ManualCropper:
    def __init__(self, image_path):
        self.image_path = image_path
        self.cropping = False
        self.ref_point = []
        self.clone = None
        self.current_rect = None
        self.resizing = False
        self.resize_point = None
        self.resize_threshold = 10  # Pixel range to detect resize handle

    def crop(self, brand, model, part):
        image = cv2.imread(self.image_path)
        height, width = image.shape[:2]

        # Resize the image if it exceeds a certain size (e.g., 800x600)
        max_width, max_height = 800, 600
        if width > max_width or height > max_height:
            scale = min(max_width / width, max_height / height)
            image = cv2.resize(image, (int(width * scale), int(height * scale)))

        self.clone = image.copy()  # Save the clone for resetting
        cv2.namedWindow("Image")
        cv2.setMouseCallback("Image", self.click_and_crop)  # ✅ This function is now added

        while True:
            temp_image = self.clone.copy()

            # Draw the selected cropping rectangle
            if len(self.ref_point) == 2:
                cv2.rectangle(temp_image, self.ref_point[0], self.ref_point[1], (0, 255, 0), 2)
                self.draw_resize_handles(temp_image)

            cv2.imshow("Image", temp_image)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("r"):  # Reset the cropping region
                self.ref_point = []
                self.current_rect = None
                self.clone = image.copy()
            elif key == ord("c"):  # Confirm the crop
                if len(self.ref_point) == 2:
                    x1, y1 = self.ref_point[0]
                    x2, y2 = self.ref_point[1]
                    crop_img = self.clone[y1:y2, x1:x2]

                    # Generate unique filename
                    timestamp = int(time.time())  # Get current timestamp
                    output_folder = "C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection - Copy/croped/"
                    os.makedirs(output_folder, exist_ok=True)
                    output_path = os.path.join(output_folder, f"croped_image.jpg")

                    cv2.imwrite(output_path, crop_img)
                    print(f"Cropped image saved to {output_path}")
                break
            elif key == 27:  # Exit with Esc
                break

        cv2.destroyAllWindows()
        return output_path  # Return the saved image path

    def click_and_crop(self, event, x, y, flags, param):
        """Handles mouse click and drag for cropping the image."""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.ref_point = [(x, y)]
            self.cropping = True

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.cropping:
                temp_image = self.clone.copy()
                cv2.rectangle(temp_image, self.ref_point[0], (x, y), (0, 255, 0), 2)
                cv2.imshow("Image", temp_image)

        elif event == cv2.EVENT_LBUTTONUP:
            self.ref_point.append((x, y))
            self.cropping = False
            cv2.rectangle(self.clone, self.ref_point[0], self.ref_point[1], (0, 255, 0), 2)
            cv2.imshow("Image", self.clone)

    def draw_resize_handles(self, img):
        """Draw small circles at the rectangle corners to indicate resizing handles."""
        if len(self.ref_point) == 2:
            for point in self.ref_point:
                cv2.circle(img, point, 5, (0, 0, 255), -1)  # Red resize handles

    def is_near_resize_handle(self, x, y):
        """Check if the user clicked near a resize handle."""
        if len(self.ref_point) < 2:
            return False
        x1, y1 = self.ref_point[0]
        x2, y2 = self.ref_point[1]

        return abs(x - x2) < self.resize_threshold and abs(y - y2) < self.resize_threshold
