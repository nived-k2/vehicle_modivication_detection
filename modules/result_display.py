def display_results(results):
    print("\n--- Results ---")
    for part, status in results.items():
        print(f"{part.capitalize()}: {status}")

def generate_report(results, output_path="C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection - Copy/results/report.txt"):
    with open(output_path, "w") as report_file:
        report_file.write("Vehicle Modification Detection Results\n")
        for part, status in results.items():
            report_file.write(f"{part.capitalize()}: {status}\n")
