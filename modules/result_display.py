from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os
import shutil
import time

# Store modification history
MODIFICATION_HISTORY = []
REPORT_PATH = "C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection - Copy/results/modification_report.pdf"
PENALTY_RATE = 5000  # Set penalty per modification

def display_results(results):
    print("\n--- Results ---")
    for part, status in results.items():
        print(f"{part.capitalize()}: {status}")

def append_modification(brand, model, part, status, cropped_image=None):
    timestamp = int(time.time())

    # ✅ Only copy an image if provided
    if cropped_image:
        unique_image_path = f"C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection - Copy/results/cropped_{brand}_{model}_{part}_{timestamp}.jpg"
        shutil.copy(cropped_image, unique_image_path)
    else:
        unique_image_path = None  # ✅ No image for exhaust test

    MODIFICATION_HISTORY.append({
        "brand": brand,
        "model": model,
        "part": part,
        "status": status,
        "cropped_image": unique_image_path  # Store None if no image
    })


def reset_report():
    """Reset modification history and delete the old report when the system starts."""
    global MODIFICATION_HISTORY
    MODIFICATION_HISTORY = []  # Clear all previous modifications

    # Delete existing PDF report if it exists
    if os.path.exists(REPORT_PATH):
        os.remove(REPORT_PATH)
        print(f"Previous report deleted: {REPORT_PATH}")

def generate_report(final=False):
    """Generate a cumulative PDF report of all modifications."""
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)

    c = canvas.Canvas(REPORT_PATH, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(180, height - 50, "Vehicle Modification Detection Report")

    c.setFont("Helvetica", 12)
    y_position = height - 100

    total_modifications = len(MODIFICATION_HISTORY)
    total_penalty = total_modifications * PENALTY_RATE

    c.drawString(100, y_position, f"Total Modifications: {total_modifications}")
    c.drawString(100, y_position - 20, f"Total Penalty: ₹{total_penalty}")

    y_position -= 50

    for mod in MODIFICATION_HISTORY:
        c.drawString(100, y_position, f"Brand: {mod['brand']} | Model: {mod['model']} | Part: {mod['part']} | Status: {mod['status']}")

        # ✅ Only add image if it exists
        if mod["cropped_image"] and os.path.exists(mod["cropped_image"]):
            img = ImageReader(mod["cropped_image"])
            c.drawImage(img, 100, y_position - 100, width=150, height=100)
            y_position -= 120  # Adjust spacing for image

        y_position -= 40  # Move down for next entry

    c.save()
    print(f"Report saved to {REPORT_PATH}")


def finalize_report():
    """Call this function before closing the system to finalize the report."""
    generate_report(final=True)
