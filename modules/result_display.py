from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os
def display_results(results):
    print("\n--- Results ---")
    for part, status in results.items():
        print(f"{part.capitalize()}: {status}")

def generate_report(modifications, total_modifications, total_penalty, output_path=None):
    # Set default report path if not provided
    if output_path is None:
        output_path = "C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection - Copy/results/report.pdf"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Ensure directory exists

    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(180, height - 50, "Vehicle Modification Detection Report")

    # Summary
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 100, f"Total Modifications: {total_modifications}")
    c.drawString(100, height - 120, f"Total Penalty: ₹{total_penalty}")

    y_position = height - 150  # Start position for modification details

    for mod in modifications:
        brand, model, part, cropped_image, status = (
            mod["brand"], mod["model"], mod["part"], mod["cropped_image"], mod["status"]
        )

        # Vehicle Info
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y_position, f"Brand: {brand}")
        c.drawString(300, y_position, f"Model: {model}")
        y_position -= 20

        c.setFont("Helvetica", 12)
        c.drawString(100, y_position, f"Part: {part}")
        c.drawString(300, y_position, f"Status: {status}")
        y_position -= 20

        # Add Cropped Image
        if os.path.exists(cropped_image):
            img = ImageReader(cropped_image)
            c.drawImage(img, 100, y_position - 100, width=150, height=100)
            y_position -= 120  # Move down to avoid overlap

        y_position -= 40  # Space between parts

    c.save()
    print(f"Report saved to {output_path}")