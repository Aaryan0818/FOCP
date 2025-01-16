import json
from tabulate import tabulate

# Initialize the driver dictionary
f1_driver = {}

try:
    # Load driver data from f1_drivers.txt
    with open("f1_drivers.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line:
                car_number, unique_code, name, team_name = line.split(',')
                f1_driver[unique_code] = {
                    "Name": name,
                    "Car Number": car_number,
                    "Team Name": team_name,
                    "Fastest Lap Time": None,  # Initially None
                    "Total Laps": 0,
                    "Average Lap Time": 0.0,
                    "Total Lap Time": 0.0
                }
    
    # Function to process lap times
    def process_lap_times(file_name):
        with open(file_name, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        driver_code, lap_time = line[:3], float(line[3:])
                        if driver_code in f1_driver:
                            driver_data = f1_driver[driver_code]
                            driver_data["Total Lap Time"] += lap_time
                            driver_data["Total Laps"] += 1
                            
                            # Update fastest lap time
                            if driver_data["Fastest Lap Time"] is None or lap_time < driver_data["Fastest Lap Time"]:
                                driver_data["Fastest Lap Time"] = lap_time
                    except (ValueError, IndexError):
                        # Skip malformed lines
                        continue
    
    # Process lap times from all files
    for lap_file in ["lap_times_1.txt", "lap_times_2.txt", "lap_times_3.txt"]:
        process_lap_times(lap_file)
    
    # Prepare data for tabular display
    table_data = []
    for unique_code, details in f1_driver.items():
        if details["Total Laps"] > 0:
            details["Average Lap Time"] = details["Total Lap Time"] / details["Total Laps"]
        
        table_data.append([
            details["Name"],
            unique_code,
            details["Car Number"],
            details["Team Name"],
            details["Total Laps"],
            f"{details['Fastest Lap Time']:.3f}" if details["Fastest Lap Time"] else "N/A",
            f"{details['Average Lap Time']:.3f}",
            f"{details['Total Lap Time']:.3f}"
        ])
    
    # Sort data by fastest lap time
    table_data.sort(key=lambda x: float(x[5]) if x[5] != "N/A" else float("inf"))
    
    # Define headers
    headers = ["Driver Name", "Unique Code", "Car Number", "Team Name", "Total Laps", "Fastest Lap Time", "Average Lap Time", "Total Lap Time"]
    
    # Display the table
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

except FileNotFoundError as e:
    print(f"Error: {e}")
