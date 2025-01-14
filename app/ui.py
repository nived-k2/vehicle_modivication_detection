import tkinter as tk
from tkinter import filedialog, ttk
from app.manual_cropping import ManualCropper
from app.main import main
from modules.exhaust_testing import test_exhaust_sound

class VehicleModificationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Modification Detection")

        # Image Upload
        tk.Label(root, text="Upload Image:").grid(row=0, column=0, padx=10, pady=10)
        tk.Button(root, text="Browse Image", command=self.upload_image).grid(row=0, column=1, padx=10, pady=10)

        # Brand Selection
        tk.Label(root, text="Select Brand:").grid(row=2, column=0, padx=10, pady=10)
        self.brand_var = tk.StringVar()
        self.brand_dropdown = ttk.Combobox(root, textvariable=self.brand_var, state="readonly")
        self.brand_dropdown['values'] = ["Bajaj", "tvs", "yamaha"]
        self.brand_dropdown.grid(row=2, column=1, padx=10, pady=10)
        self.brand_dropdown.bind("<<ComboboxSelected>>", self.update_model_dropdown)

        # Model Selection
        tk.Label(root, text="Select Model:").grid(row=3, column=0, padx=10, pady=10)
        self.model_var = tk.StringVar()
        self.model_dropdown = ttk.Combobox(root, textvariable=self.model_var, state="readonly")
        self.model_dropdown.grid(row=3, column=1, padx=10, pady=10)

        # Part Selection
        tk.Label(root, text="Select Part Type:").grid(row=4, column=0, padx=10, pady=10)
        self.part_var = tk.StringVar()
        self.part_dropdown = ttk.Combobox(root, textvariable=self.part_var, state="readonly")
        self.part_dropdown['values'] = ["Exhaust", "Headlight"]
        self.part_dropdown.grid(row=4, column=1, padx=10, pady=10)

        # Manual Crop
        tk.Button(root, text="Manual Crop", command=self.manual_crop).grid(row=5, column=0, padx=10, pady=10)

        # Start Detection
        tk.Button(root, text="Start Detection", command=self.start_detection).grid(row=5, column=1, padx=10, pady=10)

        # Test Exhaust Button
        tk.Button(root, text="Test Exhaust", command=self.test_exhaust).grid(row=6, column=0, padx=10, pady=10)

        # Results Display
        self.result_text = tk.Text(root, height=10, width=50)
        self.result_text.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def update_model_dropdown(self, event):
        brand = self.brand_var.get()
        models = {
            "Bajaj": ["Dominar", "Pulsar 150", "Pulsar 220"],
            "tvs": ["raider", "RR310", "Ronnin"],
            "yamaha": ["Shine", "Unicorn", "CBR"]
        }
        self.model_dropdown['values'] = models.get(brand, [])
        self.model_var.set("")  # Clear previous selection

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if self.image_path:
            self.result_text.insert(tk.END, f"Image Uploaded: {self.image_path}\n")
        else:
            self.result_text.insert(tk.END, "No image selected.\n")

    def manual_crop(self):
        if not hasattr(self, 'image_path') or not self.image_path:
            self.result_text.insert(tk.END, "Please upload an image first.\n")
            return
        cropper = ManualCropper(self.image_path)
        cropper.crop()

    def start_detection(self):
        brand = self.brand_var.get()
        model = self.model_var.get()
        part = self.part_var.get()

        if not brand or not model or not part:
            self.result_text.insert(tk.END, "Please select brand, model, and part.\n")
            return
        if not hasattr(self, 'image_path') or not self.image_path:
            self.result_text.insert(tk.END, "Please upload an image first.\n")
            return

        self.result_text.insert(tk.END, f"Starting detection for {brand} {model} - {part}...\n")
        try:
            results = main(self.image_path, brand, model, part)
            self.result_text.insert(tk.END, "--- Results ---\n")
            for key, value in results.items():
                self.result_text.insert(tk.END, f"{key}: {value}\n")
        except Exception as e:
            self.result_text.insert(tk.END, f"Error during detection: {str(e)}\n")

    def test_exhaust(self):
        # Prompt for file or microphone input
        self.result_text.insert(tk.END, "Testing Exhaust...\n")
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.aac")])
        if file_path:
            result = test_exhaust_sound(file_path)
            self.result_text.insert(tk.END, f"Exhaust Test Result: {result}\n")
        else:
            self.result_text.insert(tk.END, "No audio file selected.\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = VehicleModificationApp(root)
    root.mainloop()
