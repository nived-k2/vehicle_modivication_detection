import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from app.manual_cropping import ManualCropper
from app.main import main
import subprocess


class VehicleModificationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Modification Detection")
        self.modification_count = 0
        self.penalty_rate = 5000  # Penalty per modification

        # Upload Section
        upload_frame = tk.LabelFrame(root, text="Upload Image", padx=10, pady=10)
        upload_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        tk.Button(upload_frame, text="Browse Image", command=self.upload_image).pack()

        # Selection Section
        selection_frame = tk.LabelFrame(root, text="Vehicle Details", padx=10, pady=10)
        selection_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        tk.Label(selection_frame, text="Select Brand:").grid(row=0, column=0)
        self.brand_var = tk.StringVar()
        self.brand_dropdown = ttk.Combobox(selection_frame, textvariable=self.brand_var, state="readonly")
        self.brand_dropdown['values'] = ["Bajaj", "tvs", "Yamaha"]
        self.brand_dropdown.grid(row=0, column=1)
        self.brand_dropdown.bind("<<ComboboxSelected>>", self.update_model_dropdown)

        tk.Label(selection_frame, text="Select Model:").grid(row=1, column=0)
        self.model_var = tk.StringVar()
        self.model_dropdown = ttk.Combobox(selection_frame, textvariable=self.model_var, state="readonly")
        self.model_dropdown.grid(row=1, column=1)

        tk.Label(selection_frame, text="Select Part Type:").grid(row=2, column=0)
        self.part_var = tk.StringVar()
        self.part_dropdown = ttk.Combobox(selection_frame, textvariable=self.part_var, state="readonly")
        self.part_dropdown['values'] = ["Exhaust", "Headlight"]
        self.part_dropdown.grid(row=2, column=1)

        # Action Buttons
        button_frame = tk.LabelFrame(root, text="Actions", padx=10, pady=10)
        button_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        tk.Button(button_frame, text="Manual Crop", command=self.manual_crop).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Start Detection", command=self.start_detection).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Test Exhaust", command=self.run_exhaust_test).grid(row=0, column=2, padx=5, pady=5)

        # Results Display
        self.result_text = tk.Text(root, height=12, width=60)
        self.result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Penalty Display
        self.penalty_label = tk.Label(root, text="Penalty: ₹0", font=("Arial", 12, "bold"))
        self.penalty_label.grid(row=4, column=0, columnspan=2, pady=10)

        # Exit Button
        tk.Button(root, text="Exit", command=self.exit_app, bg="red", fg="white", font=("Arial", 12, "bold")).grid(row=5, column=0, columnspan=2, pady=10)

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if self.image_path:
            self.result_text.insert(tk.END, f"Image Uploaded: {self.image_path}\n")
        else:
            self.result_text.insert(tk.END, "No image selected.\n")

    def update_model_dropdown(self, event):
        brand = self.brand_var.get()
        models = {
            "Bajaj": ["Dominar", "Pulsar 150", "Pulsar 220"],
            "tvs": ["raider", "RR310", "Ronin"],
            "Yamaha": ["R15", "MT-15", "FZ-X"]
        }
        self.model_dropdown['values'] = models.get(brand, [])
        self.model_var.set("")  # Clear previous selection

    def manual_crop(self):
        if not hasattr(self, 'image_path') or not self.image_path:
            self.result_text.insert(tk.END, "Please upload an image first.\n")
            return
        brand = self.brand_var.get()
        model = self.model_var.get()
        part = self.part_var.get()
        cropper = ManualCropper(self.image_path, brand, model, part)
        cropper.crop()

    def start_detection(self):
        brand, model, part = self.brand_var.get(), self.model_var.get(), self.part_var.get()
        if not brand or not model or not part:
            self.result_text.insert(tk.END, "Please select brand, model, and part.\n")
            return
        if not hasattr(self, 'image_path') or not self.image_path:
            self.result_text.insert(tk.END, "Please upload an image first.\n")
            return

        self.result_text.insert(tk.END, f"Starting detection for {brand} {model} - {part}...\n")
        try:
            results = main(self.image_path, brand, model, part)

            for key, value in results.items():
                self.result_text.insert(tk.END, f"{key}: {value}\n")
                if value == "Modified" or "Modification Detected" in value:  # Fix here
                    self.modification_count += 1

            self.update_penalty()
            if not messagebox.askyesno("Continue Checking?", "Do you want to continue checking other parts?"):
                self.show_final_penalty()
        except Exception as e:
            self.result_text.insert(tk.END, f"Error during detection: {str(e)}\n")
    def show_final_penalty(self):
        penalty = self.modification_count * self.penalty_rate
        self.result_text.insert(tk.END, f"\n--- Final Status ---\nModifications Detected: {self.modification_count}\nTotal Penalty: ₹{penalty}\n")

    def update_penalty(self):
        penalty = self.modification_count * self.penalty_rate
        self.penalty_label.config(text=f"Penalty: ₹{penalty}")

    def run_exhaust_test(self):
        self.result_text.insert(tk.END, "Starting Exhaust Test...\n")
        self.root.update()

        try:
            result = subprocess.run(["python", "exhaust_testing.py"], capture_output=True, text=True)
            if result.returncode == 0:
                status = result.stdout.strip().split("\n")[-1].strip()
                if status == "MODIFIED":
                    self.result_text.insert(tk.END, f"Exhaust Test Result: {status}\n")
                    self.modification_count += 1  # Ensure modification count is updated
                    self.update_penalty()
                elif status == "NOT MODIFIED":
                    self.result_text.insert(tk.END, "Exhaust Test Result: NOT MODIFIED\n")
                else:
                    self.result_text.insert(tk.END, f"Unexpected output: {status}\n")
            else:
                self.result_text.insert(tk.END, f"Error: {result.stderr.strip()}\n")

            if not messagebox.askyesno("Continue Checking?", "Do you want to continue checking other parts?"):
                self.show_final_penalty()

        except Exception as e:
            self.result_text.insert(tk.END, f"Error running exhaust test: {str(e)}\n")

        self.result_text.see(tk.END)
        self.root.update()
    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = VehicleModificationApp(root)
    root.mainloop()
