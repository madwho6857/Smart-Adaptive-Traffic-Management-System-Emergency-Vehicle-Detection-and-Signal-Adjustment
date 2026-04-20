import networkx as nx
import matplotlib.pyplot as plt
import re

# Function to read the daily vehicle log and extract vehicle counts and status
def read_vehicle_log(log_file):
    vehicle_data = []
    with open(log_file, 'r') as file:
        for line in file:
            # Extract relevant information from each log line
            match = re.search(r"Total Vehicle Count: (\d+), Emergency Vehicle Count: (\d+), Traffic Light Status: (\w+)", line)
            if match:
                vehicle_count = int(match.group(1))
                emergency_vehicle_count = int(match.group(2))
                traffic_light_status = match.group(3)
                vehicle_data.append({
                    "vehicle_count": vehicle_count,
                    "emergency_vehicle_count": emergency_vehicle_count,
                    "traffic_light_status": traffic_light_status
                })
    return vehicle_data

# Determine traffic signal behavior based on vehicle count and emergency vehicle presence
def determine_signal_status(vehicle_count, emergency_vehicle_count, traffic_light_status):
    # If emergency vehicle is present, change traffic light to green
    if emergency_vehicle_count > 0:
        return "Override - Green for Emergency"
    # Otherwise, adjust based on vehicle count and existing traffic light status
    if traffic_light_status == "Green":
        return "Normal Green"
    elif traffic_light_status == "Red":
        return "Normal Red"
    else:
        return "Unknown Status"

# File path to the log
log_path = 'daily_vehicle_log.txt'

# Read vehicle data from the log
vehicle_data = read_vehicle_log(log_path)

# Create the knowledge graph
G = nx.Graph()
G.add_node("Traffic Light", type="Controller")

# Add vehicle-related nodes and edges based on the log data
for idx, entry in enumerate(vehicle_data):
    data_name = f"Data {idx + 1}"  # Change lane name to Data1, Data2, etc.
    vehicle_count = entry["vehicle_count"]
    emergency_vehicle_count = entry["emergency_vehicle_count"]
    traffic_light_status = entry["traffic_light_status"]

    traffic_status = determine_signal_status(vehicle_count, emergency_vehicle_count, traffic_light_status)

    G.add_node(data_name, vehicle_count=vehicle_count, traffic_status=traffic_status)
    G.add_edge(data_name, "Traffic Light", relationship=f"{traffic_status} (Count: {vehicle_count}, Emergency: {emergency_vehicle_count})")

# Add emergency vehicle logic
G.add_node("Emergency Vehicle", type="Emergency")
for idx in range(len(vehicle_data)):
    G.add_edge("Emergency Vehicle", f"Data {idx + 1}", relationship="Priority in Data")

# Draw the graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)
node_colors = ["red" if n == "Emergency Vehicle" else "lightblue" for n in G.nodes()]
node_sizes = [3500 if n == "Traffic Light" else 2500 for n in G.nodes()]

nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=node_sizes, font_weight='bold', font_size=10)
edge_labels = nx.get_edge_attributes(G, 'relationship')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

plt.title("Dynamic Traffic Knowledge Graph Based on Vehicle Log", fontsize=14)
plt.tight_layout()
plt.show()
