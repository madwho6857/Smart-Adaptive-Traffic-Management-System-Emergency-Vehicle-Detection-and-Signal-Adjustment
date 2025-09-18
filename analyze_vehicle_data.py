import pandas as pd

# Load the log data
log_file_path = r"C:\Users\Asus\OneDrive\Desktop\college\Smart-Adaptive-Traffic-Management-System-main\Smart-Adaptive-Traffic-Management-System-main\daily_vehicle_log.txt"

# Parse log data into a dataframe
log_data = []
with open(log_file_path, "r") as file:
    for line in file:
        timestamp, data = line.split('] ', 1)
        timestamp = timestamp.strip('[')
        total_vehicles = int(data.split('Total Vehicle Count: ')[1].split(',')[0].strip())
        emergency_vehicles = int(data.split('Emergency Vehicle Count: ')[1].split(',')[0].strip())
        traffic_status = data.split('Traffic Light Status: ')[1].strip()
        
        log_data.append([timestamp, total_vehicles, emergency_vehicles, traffic_status])

# Convert to DataFrame
df = pd.DataFrame(log_data, columns=["Timestamp", "Total Vehicles", "Emergency Vehicles", "Traffic Status"])

# Calculate average counts
avg_total_vehicles = df["Total Vehicles"].mean()
avg_emergency_vehicles = df["Emergency Vehicles"].mean()

print(f"Average Total Vehicles: {avg_total_vehicles}")
print(f"Average Emergency Vehicles: {avg_emergency_vehicles}")
