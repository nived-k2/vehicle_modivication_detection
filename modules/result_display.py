from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os
def display_results(results):
    print("\n--- Results ---")
    for part, status in results.items():
        print(f"{part.capitalize()}: {status}")

def generate_report(modifications, total_modifications, total_penalty, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(180, height - 50, "Vehicle Modification Detection Report")

    c.setFont("Helvetica", 12)
    c.drawString(100, height - 100, f"Total Modifications: {total_modifications}")
    c.drawString(100, height - 120, f"Total Penalty: ₹{total_penalty}")

    y_position = height - 150
    for mod in modifications:
        c.drawString(100, y_position, f"Brand: {mod['brand']} | Model: {mod['model']} | Part: {mod['part']} | Status: {mod['status']}")
        if os.path.exists(mod["cropped_image"]):
            img = ImageReader(mod["cropped_image"])
            c.drawImage(img, 100, y_position - 100, width=150, height=100)
            y_position -= 120
        y_position -= 40

    c.save()
    print(f"Report saved to {output_path}")