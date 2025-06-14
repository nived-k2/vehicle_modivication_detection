## ✅ How It Works

1️⃣ **Part Detection**  
   - The system uses a general YOLOv8 model to find the part (e.g., exhaust).  
   - If nothing is found → show *"No part detected"*.

2️⃣ **Cropping**  
   - The detected bounding box automatically crops out the part for accurate checking.

3️⃣ **Load Brand-Model-Specific Models**  
   - The detected part’s brand, model, and part name decide which YOLO model + autoencoder to load.

4️⃣ **Detailed Detection + Feature Extraction**  
   - The part-specific YOLO model double-checks the part if needed.
   - Features are extracted from the cropped region.

5️⃣ **Anomaly Detection (Autoencoder)**  
   - The autoencoder checks if the cropped part’s pattern matches the stock pattern.
   - It calculates error scores and compares them to a pre-set threshold (`error_statistics.json`).

6️⃣ **Final Result**  
   - If error score is low → *Stock*  
   - If error score is high or no model found → *Modified*

**For detailed understaning documentation of the project is included(Two_Wheeler_Vehicle_Modification_Detection_System(3).pdf
