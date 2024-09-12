import os
import glob
import time
import csv
from datetime import datetime

# Load 1-Wire kernel modules
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Base directory for the 1-Wire devices
base_dir = '/sys/bus/w1/devices/'

def find_sensors():
    # Find all sensor folders
    return glob.glob(base_dir + '28*')

def read_temp_raw(device_file):
    with open(device_file, 'r') as f:
        lines = f.readlines()
    return lines

def read_temp(device_file):
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(device_file)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

def write_to_csv(header, data):
    file_path = '/home/pi/Sherlock/data/Thermal/temperature_readings.csv'
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if header and not os.path.getsize(file_path):
            writer.writerow(header)
        if data is not None:
            writer.writerow(data)

# Detect all sensors and create CSV header
device_folders = find_sensors()
device_serials = [os.path.basename(device_folder) for device_folder in device_folders]

# Print sensor serial numbers
print("Detected Sensors:")
for serial in device_serials:
    print(serial)

# Create CSV header with serial numbers
csv_header = ['Timestamp'] + device_serials

# Write header to CSV if file doesn't exist
if not os.path.isfile('/home/pi/Sherlock/data/Thermal/temperature_readings.csv'):
    write_to_csv(csv_header, None)

try:
    # Main loop to read temperature from all sensors and write to CSV
    while True:
        device_folders = find_sensors()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        temperatures = [timestamp]

        for device_folder in device_folders:
            device_file = device_folder + '/w1_slave'
            temp_c = read_temp(device_file)
            temperatures.append(temp_c)
        
        # Print the current temperatures along with serial numbers
        print(f"\nTemperatures at {timestamp}:")
        for serial, temp in zip(device_serials, temperatures[1:]):
            print(f"{serial}: {temp}°C")
        
        # Write data to CSV file
        write_to_csv(None, temperatures)
        
        # Wait 15 minutes (900 seconds) before the next reading
        time.sleep(900)

except KeyboardInterrupt:
    print("\nProgram stopped by user.")
