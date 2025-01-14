import cv2
import os


class ManualCropper:
    def __init__(self, image_path):
        self.image_path = image_path
        self.cropping = False
        self.ref_point = []
        self.clone = None  # Store the cloned image here

    def crop(self):
        image = cv2.imread(self.image_path)
        height, width = image.shape[:2]

        # Resize the image if it exceeds a certain size (e.g., 800x600)
        max_width, max_height = 800, 600
        if width > max_width or height > max_height:
            scale = min(max_width / width, max_height / height)
            image = cv2.resize(image, (int(width * scale), int(height * scale)))

        self.clone = image.copy()  # Save the clone for resetting
        cv2.namedWindow("Image")
        cv2.setMouseCallback("Image", self.click_and_crop)

        while True:
            cv2.imshow("Image", image)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("r"):  # Reset the cropping region
                image = self.clone.copy()
            elif key == ord("c"):  # Confirm the crop
                if len(self.ref_point) == 2:
                    x1, y1 = self.ref_point[0]
                    x2, y2 = self.ref_point[1]
                    crop_img = self.clone[y1:y2, x1:x2]

                    # Save cropped image to the desired path
                    output_path = "C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection - Copy/data/autoencoder/crop/test/cropped_image.jpg"
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Ensure the directory exists
                    cv2.imwrite(output_path, crop_img)
                    print(f"Cropped image saved to {output_path}")
                break
            elif key == 27:  # Exit with Esc
                break

        cv2.destroyAllWindows()

    def click_and_crop(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.ref_point = [(x, y)]
            self.cropping = True
        elif event == cv2.EVENT_MOUSEMOVE and self.cropping:
            temp_image = self.clone.copy()  # Use the stored clone
            cv2.rectangle(temp_image, self.ref_point[0], (x, y), (0, 255, 0), 2)
            cv2.imshow("Image", temp_image)
        elif event == cv2.EVENT_LBUTTONUP:
            self.ref_point.append((x, y))
            self.cropping = False
            cv2.rectangle(self.clone, self.ref_point[0], self.ref_point[1], (0, 255, 0), 2)
            cv2.imshow("Image", self.clone)
