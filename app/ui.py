import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from app.manual_cropping import ManualCropper
from app.main import main
import subprocess
import os


class VehicleModificationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Modification Detection")
        self.modification_count = 0  # To track the number of modifications detected
        self.penalty_rate = 5000  # Penalty rate per modification

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
        self.result_text = tk.Text(root, height=15, width=60)
        self.result_text.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
        self.result_text.config(state=tk.DISABLED)

    def update_model_dropdown(self, event):
        brand = self.brand_var.get()
        models = {
            "Bajaj": ["Dominar", "Pulsar 150", "Pulsar 220"],
            "tvs": ["Raider", "RR310", "Ronin"],
            "yamaha": ["Shine", "Unicorn", "CBR"]
        }
        self.model_dropdown['values'] = models.get(brand, [])
        self.model_var.set("")  # Clear previous selection

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if self.image_path:
            self.append_result(f"Image Uploaded: {self.image_path}\n")
        else:
            self.append_result("No image selected.\n")

    def manual_crop(self):
        if not hasattr(self, 'image_path') or not self.image_path:
            self.append_result("Please upload an image first.\n")
            return
        brand = self.brand_var.get()
        model = self.model_var.get()
        part = self.part_var.get()

        if not brand or not model or not part:
            self.append_result("Please select brand, model, and part before cropping.\n")
            return

        cropper = ManualCropper(self.image_path, brand, model, part)
        cropper.crop()

    def start_detection(self):
        brand = self.brand_var.get()
        model = self.model_var.get()
        part = self.part_var.get()

        if not brand or not model or not part:
            self.append_result("Please select brand, model, and part.\n")
            return
        if not hasattr(self, 'image_path') or not self.image_path:
            self.append_result("Please upload an image first.\n")
            return

        self.append_result(f"Starting detection for {brand} {model} - {part}...\n")
        try:
            results = main(self.image_path, brand, model, part)
            for key, value in results.items():
                self.append_result(f"{key}: {value}\n")
                if value == "Modified":
                    self.modification_count += 1  # Increase modification count

            # Ask if the user wants to continue
            continue_checking = messagebox.askyesno(
                "Continue Checking?",
                "Do you want to continue checking other parts?"
            )
            if not continue_checking:
                self.show_final_penalty()
        except Exception as e:
            self.append_result(f"Error during detection: {str(e)}\n")

    def test_exhaust(self):
        """Run the exhaust testing process."""
        script_path = os.path.abspath("exhaust_testing.py")  # Adjust to the correct script location

        if not os.path.exists(script_path):
            self.append_result(f"Error: {script_path} not found.\n")
            return

        try:
            # Run the exhaust_testing.py script in a subprocess
            process = subprocess.Popen(["python", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            # Capture and display the output
            if stdout:
                self.append_result(f"Output: {stdout.decode('utf-8')}\n")
            if stderr:
                self.append_result(f"Error: {stderr.decode('utf-8')}\n")
        except Exception as e:
            self.append_result(f"Error running exhaust testing: {str(e)}\n")

    def append_result(self, text):
        """Safely update the result text box."""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state=tk.DISABLED)

    def show_final_penalty(self):
        """Calculate and display the final penalty."""
        penalty = self.modification_count * self.penalty_rate
        self.append_result("\n--- Final Status ---\n")
        self.append_result(f"Modifications Detected: {self.modification_count}\n")
        self.append_result(f"Total Penalty: ₹{penalty}\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = VehicleModificationApp(root)
    root.mainloop()
