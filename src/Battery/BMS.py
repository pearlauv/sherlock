import serial
import time
import csv
from datetime import datetime

# USB Serial Communication
SERIAL_PORT = '/dev/ttyUSB'
BAUD_RATE = 9600  # Adjust to your device's settings

#Data File
CSV_FILE = '/home/pi/Sherlock/data/Battery/battery_data.csv'

def read_data():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            # Request State of Charge (SOC)
            command_soc = b'\x01\x03\x00\x00\x00\x02\xC4\x0B'  # Replace with actual SOC command
            ser.write(command_soc)
            time.sleep(1)
            response_soc = ser.read(7)  # Adjust length based on expected response
            
            # Request State of Health (SOH)
            command_soh = b'\x01\x03\x00\x01\x00\x01\xD5\xC6'  # Replace with actual SOH command
            ser.write(command_soh)
            time.sleep(1)
            response_soh = ser.read(7)  # Adjust length based on expected response
            
            # Request Power Output
            command_power = b'\x01\x03\x00\x02\x00\x01\xD5\xC6'  # Replace with actual Power Output command
            ser.write(command_power)
            time.sleep(1)
            response_power = ser.read(7)  # Adjust length based on expected response

            if response_soc and response_soh and response_power:
                # Parse SOC response
                soc = response_soc[3]  # Adjust based on your protocol
                # Parse SOH response
                soh = response_soh[3]  # Adjust based on your protocol
                # Parse Power Output response
                power_output = (response_power[3] << 8) | response_power[4]  # Adjust for your protocol

                # Get current timestamp
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Write to CSV
                with open(CSV_FILE, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    # Write header if the file is empty
                    if file.tell() == 0:
                        writer.writerow(['Timestamp', 'SOC', 'SOH', 'Power Output (W)'])
                    # Write data
                    writer.writerow([timestamp, soc, soh, power_output])
                
                print(f"Timestamp: {timestamp}")
                print(f"SOC: {soc}")
                print(f"SOH: {soh}")
                print(f"Power Output: {power_output} W")
            else:
                print("No response received.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    read_data()
