def adjust_green_signal_time(vehicle_count):
    base_green_time = 30  # seconds
    vehicle_multiplier = 2  # per vehicle
    return base_green_time + (vehicle_count * vehicle_multiplier)

def main():
    try:
        path = r"C:\Users\Asus\Downloads\Smart-Adaptive-Traffic-Management-System-main\Smart-Adaptive-Traffic-Management-System-main\vehicle_count.txt"
        with open(path, "r") as file:
            lines = file.readlines()

            # Find last "Total Vehicle Count"
            for line in reversed(lines):
                if "Total Vehicle Count" in line:
                    vehicle_count = int(line.strip().split(":")[1])
                    break
            else:
                print("No vehicle count found.")
                return

        green_time = adjust_green_signal_time(vehicle_count)
        print("Adjusted Green Signal Time:", green_time, "seconds")

    except (ValueError, FileNotFoundError) as e:
        print("Error reading vehicle count from file:", e)

if __name__ == "__main__":
    main()
