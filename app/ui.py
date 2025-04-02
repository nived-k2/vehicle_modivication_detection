import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from app.manual_cropping import crop_image
from app.main import main
from modules.result_display import generate_report, finalize_report, append_modification, reset_report
from models.yolo import YOLOModel
import subprocess
import os

class VehicleModificationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Modification Detection")

        # ✅ Reset Report on Startup
        reset_report()

        self.part_detection_model = YOLOModel("C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection - Copy/models/best (2).pt")
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

        # Action Buttons
        button_frame = tk.LabelFrame(root, text="Actions", padx=10, pady=10)
        button_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        tk.Button(button_frame, text="Start Detection", command=self.start_detection).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Test Exhaust", command=self.run_exhaust_test).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(button_frame, text="Clear", command=self.clear_ui).grid(row=0, column=3, padx=5, pady=5)

        # Results Display
        self.result_text = tk.Text(root, height=12, width=60)
        self.result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Penalty Display
        self.penalty_label = tk.Label(root, text="Penalty: ₹0", font=("Arial", 12, "bold"))
        self.penalty_label.grid(row=4, column=0, columnspan=2, pady=10)

        # Exit Button
        tk.Button(root, text="Exit", command=self.exit_app, bg="red", fg="white", font=("Arial", 12, "bold")).grid(row=5, column=0, columnspan=2, pady=10)

        root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Ensure report finalization on exit

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if self.image_path:
            self.result_text.insert(tk.END, f"Image Uploaded: {self.image_path}\n")
        else:
            self.result_text.insert(tk.END, "No image selected.\n")

    def clear_ui(self):
        """Prompts to download the report before resetting the UI and deleting the old report."""
        from modules.result_display import reset_report, download_report  # Import necessary functions

        if os.path.exists(
                "C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection - Copy/results/modification_report.pdf"):
            # Ask if the user wants to download the report before clearing
            response = messagebox.askyesno("Download Report",
                                           "Do you want to download the current report before resetting?")

            if response:  # If user chooses "Yes"
                download_report()  # Allow user to save report before deletion

        reset_report()  # Deletes the report and resets the modification history

        # Reset UI Elements
        self.brand_var.set("")  # Reset brand dropdown
        self.model_var.set("")  # Reset model dropdown
        self.result_text.delete("1.0", tk.END)  # Clear results text
        self.modification_count = 0  # Reset modification count
        self.penalty_label.config(text="Penalty: ₹0")  # Reset penalty display
        if hasattr(self, 'image_path'):
            del self.image_path  # Remove uploaded image path

        messagebox.showinfo("Reset", "UI has been reset! A new report will be generated.")

    def on_closing(self):
        """Finalize the report and close the application safely."""
        finalize_report()  # Ensures all modifications and penalties are logged before exit
        self.root.destroy()

    def update_model_dropdown(self, event):
        brand = self.brand_var.get()
        models = {
            "Bajaj": ["Dominar", "Pulsar 150", "Pulsar 220"],
            "tvs": ["raider", "RR310", "Ronin"],
            "Yamaha": ["R15", "MT-15", "FZ-X"]
        }
        self.model_dropdown['values'] = models.get(brand, [])
        self.model_var.set("")  # Clear previous selection

    def start_detection(self):
        brand, model = self.brand_var.get(), self.model_var.get()
        if not brand or not model:
            self.result_text.insert(tk.END, "Please select brand and model.\n")
            return
        if not hasattr(self, 'image_path') or not self.image_path:
            self.result_text.insert(tk.END, "Please upload an image first.\n")
            return

        # Detect part using YOLO
        detections = self.part_detection_model.detect(self.image_path)
        if not detections:
            messagebox.showerror("Error", "No part detected. Please upload a clearer image.")
            return

        detected_parts = [d['part'] for d in detections]  # Get all detected parts
        detected_parts_str = ", ".join(detected_parts)
        self.result_text.insert(tk.END, f"Detected Parts: {detected_parts_str}\n")

        # Proceed with main detection process
        for detected_part in detected_parts:
            results = main(self.image_path, brand, model, detected_part)
            for key, value in results.items():
                self.result_text.insert(tk.END, f"{key}: {value}\n")
                if value == "Modified" or "Modification Detected" in value:
                    self.modification_count += 1  # Increase modification count

        self.update_penalty()
        generate_report()

    def run_exhaust_test(self):
        brand = self.brand_var.get()
        model = self.model_var.get()

        # ✅ Prevent running if brand or model is not selected
        if not brand or not model:
            messagebox.showerror("Error", "Please select a brand and model before testing the exhaust.")
            return  # Exit function
        self.result_text.insert(tk.END, "Starting Exhaust Test...\n")
        self.root.update()

        try:
            result = subprocess.run(["python", "exhaust_testing.py"], capture_output=True, text=True)
            if result.returncode == 0:
                status = result.stdout.strip().split("\n")[-1].strip()
                if status == "MODIFIED":
                    self.result_text.insert(tk.END, f"Exhaust Test Result: {status}\n")
                    self.modification_count += 1  # Increase modification count
                    self.update_penalty()
                    append_modification(self.brand_var.get(), self.model_var.get(), "exhaust", "Modified", None)
                    generate_report()
                elif status == "NOT MODIFIED":
                    self.result_text.insert(tk.END, "Exhaust Test Result: NOT MODIFIED\n")
                else:
                    self.result_text.insert(tk.END, f"Unexpected output: {status}\n")
            else:
                self.result_text.insert(tk.END, f"Error: {result.stderr.strip()}\n")

        except Exception as e:
            self.result_text.insert(tk.END, f"Error running exhaust test: {str(e)}\n")
    generate_report()
    def update_penalty(self):
        penalty = self.modification_count * self.penalty_rate
        self.penalty_label.config(text=f"Penalty: ₹{penalty}")

    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            finalize_report()  # Finalize the report before closing
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = VehicleModificationApp(root)
    root.mainloop()
