import cv2
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

# --- Load YOLO model ---
net = cv2.dnn.readNet("yolov4.weights", "yolov4.cfg")

# Load class names
with open("coco.names", "r") as f:
    classes = f.read().strip().split("\n")

# Define vehicle-related labels
vehicle_labels = ["car", "bus", "truck", "motorbike"]
emergency_like_vehicles = ["truck", "bus"]

# Load image
image_path = r"C:\Users\Asus\OneDrive\Desktop\college\Smart-Adaptive-Traffic-Management-System-main\Smart-Adaptive-Traffic-Management-System-main\withambulance.jpg"
image = cv2.imread(image_path)

if image is None:
    print("Error: Image not found!")
    exit()

height, width, _ = image.shape

# Preprocess image
blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), swapRB=True, crop=False)
net.setInput(blob)
output_layers = net.getUnconnectedOutLayersNames()
layer_outputs = net.forward(output_layers)

# Detection results
boxes, confidences, class_ids = [], [], []

# Analyze detections
for output in layer_outputs:
    for detection in output:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]

        if confidence > 0.3:
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)

            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.4)

# Count vehicles
vehicle_count = 0
emergency_vehicle_count = 0
emergency_detected = False

# Draw results
if len(indices) > 0:
    for i in indices.flatten():
        x, y, w, h = boxes[i]
        label = classes[class_ids[i]]

        if label in vehicle_labels:
            vehicle_count += 1

            if label in emergency_like_vehicles:
                emergency_vehicle_count += 1
                emergency_detected = True
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(image, "Emergency Vehicle", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            else:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

# Decide signal
traffic_light_status = "Green" if emergency_detected else "Red"
normal_vehicle_count = vehicle_count - emergency_vehicle_count

# -------------------------------
# 🔽 Log 1: Per-Run Output Logging
# -------------------------------
run_output_file = r"C:\Users\Asus\Downloads\Smart-Adaptive-Traffic-Management-System-main\Smart-Adaptive-Traffic-Management-System-main\vehicle_count.txt"
os.makedirs(os.path.dirname(run_output_file), exist_ok=True)

with open(run_output_file, "a") as f:
    f.write(f"\n--- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
    f.write(f"Total Vehicle Count: {vehicle_count}\n")
    f.write(f"Normal Vehicle Count: {normal_vehicle_count}\n")
    f.write(f"Emergency Vehicle Count: {emergency_vehicle_count}\n")
    f.write(f"Traffic Light Status: {traffic_light_status}\n")

# --------------------------------
# 🔽 Log 2: Daily Analytics Logging
# --------------------------------
daily_log_file = "daily_vehicle_log.txt"
with open(daily_log_file, "a") as f:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Total Vehicle Count: {vehicle_count}, Emergency Vehicle Count: {emergency_vehicle_count}, Traffic Light Status: {traffic_light_status}\n"
    f.write(log_entry)

# --------------------------------
# 🖼️ Show annotated image
# --------------------------------
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.imshow(image_rgb)
plt.axis('off')
plt.title("Vehicle Detection Result")
plt.show()

# --------------------------------
# 🖨️ Print summary to console
# --------------------------------
print(" Detection Complete")
print(f"Total Vehicle Count: {vehicle_count}")
print(f"Normal Vehicle Count: {normal_vehicle_count}")
print(f"Emergency Vehicle Count: {emergency_vehicle_count}")
print(f"Traffic Light Status: {traffic_light_status}")
print("Logs written to vehicle_count.txt and daily_vehicle_log.txt")
