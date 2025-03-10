import cv2
import os
import time

class ManualCropper:
    def __init__(self, image_path, brand, model, part):
        self.image_path = image_path
        self.brand = brand
        self.model = model
        self.part = part
        self.cropping = False
        self.resizing = False
        self.ref_point = []
        self.clone = None
        self.resize_threshold = 10  # Pixel range for resizing
        self.selected_region = None  # Store cropped region for resizing

    def crop(self):
        image = cv2.imread(self.image_path)
        height, width = image.shape[:2]

        # Resize the image if it exceeds a certain size (e.g., 800x600)
        max_width, max_height = 800, 600
        if width > max_width or height > max_height:
            scale = min(max_width / width, max_height / height)
            image = cv2.resize(image, (int(width * scale), int(height * scale)))

        self.clone = image.copy()  # Save original image state
        cv2.namedWindow("Image")
        cv2.setMouseCallback("Image", self.click_and_crop)

        while True:
            temp_image = self.clone.copy()  # Reset to the original image before drawing

            # Draw the cropping rectangle if points are selected
            if len(self.ref_point) == 2:
                cv2.rectangle(temp_image, self.ref_point[0], self.ref_point[1], (0, 255, 0), 2)
                self.draw_resize_handles(temp_image)

            cv2.imshow("Image", temp_image)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("r"):  # Reset the cropping region
                self.ref_point = []
                self.selected_region = None
                self.clone = image.copy()
            elif key == ord("c") and len(self.ref_point) == 2:  # Confirm crop
                x1, y1 = self.ref_point[0]
                x2, y2 = self.ref_point[1]
                crop_img = self.clone[y1:y2, x1:x2]

                # Generate a unique filename
                timestamp = int(time.time())
                output_folder = "C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection - Copy/croped/"
                os.makedirs(output_folder, exist_ok=True)
                output_path = os.path.join(output_folder, f"croped_image.jpg")

                cv2.imwrite(output_path, crop_img)
                print(f"Cropped image saved to {output_path}")
                break
            elif key == 27:  # Exit with Esc
                break

        cv2.destroyAllWindows()
        return output_path

    def click_and_crop(self, event, x, y, flags, param):
        """Handles mouse click and drag for cropping and resizing."""
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.is_near_resize_handle(x, y):
                self.resizing = True
            else:
                self.ref_point = [(x, y)]
                self.cropping = True

        elif event == cv2.EVENT_MOUSEMOVE:
            temp_image = self.clone.copy()  # Always redraw on a fresh copy

            if self.cropping:
                cv2.rectangle(temp_image, self.ref_point[0], (x, y), (0, 255, 0), 2)
            elif self.resizing and self.selected_region:
                x1, y1, _, _ = self.selected_region
                self.ref_point = [(x1, y1), (x, y)]  # Update ref_point for resizing
                cv2.rectangle(temp_image, (x1, y1), (x, y), (0, 255, 0), 2)

            cv2.imshow("Image", temp_image)

        elif event == cv2.EVENT_LBUTTONUP:
            if self.cropping:
                self.ref_point.append((x, y))
                self.cropping = False
                self.selected_region = (*self.ref_point[0], *self.ref_point[1])  # Store final crop region
            elif self.resizing:
                x1, y1, _, _ = self.selected_region
                self.ref_point = [(x1, y1), (x, y)]
                self.resizing = False

            # Redraw on a fresh copy to remove old rectangles
            temp_image = self.clone.copy()
            cv2.rectangle(temp_image, self.ref_point[0], self.ref_point[1], (0, 255, 0), 2)
            self.draw_resize_handles(temp_image)
            cv2.imshow("Image", temp_image)

    def draw_resize_handles(self, img):
        """Draws small circles at the rectangle corners for resizing."""
        if len(self.ref_point) == 2:
            for point in self.ref_point:
                cv2.circle(img, point, 5, (0, 0, 255), -1)  # Red resize handles

    def is_near_resize_handle(self, x, y):
        """Checks if the mouse click is near a resize handle."""
        if len(self.ref_point) < 2:
            return False
        x1, y1 = self.ref_point[0]
        x2, y2 = self.ref_point[1]
        return (abs(x - x2) < self.resize_threshold and abs(y - y2) < self.resize_threshold) or \
               (abs(x - x1) < self.resize_threshold and abs(y - y1) < self.resize_threshold)
