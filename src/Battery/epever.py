import serial
import time
import pandas as pd
from datetime import datetime

# Configuration
SERIAL_PORT = '/dev/ttyUSB0'  # Change this to your serial port
BAUD_RATE = 9600               # Adjust if necessary
TIMEOUT = 1                    # Timeout for serial read
CSV_FILE = 'solar_data.csv'    # Output CSV file

# Function to read solar data
def read_solar_data():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT) as 
ser:
            # Send command to request SoC, SoH, and power output for PV1 
and PV2
            command = b'\x01\x03\x00\x00\x00\x05\xC5\xCD'  # Example 
command (modify as needed)
            ser.write(command)

            # Wait for a response
            time.sleep(1)
            response = ser.read(11)  # Adjust based on expected response 
length

            if response:
                # Parse the response (modify as per your device's 
protocol)
                soc = response[3]        # Example parsing for SoC
                soh = response[4]        # Example parsing for SoH
                power_output_pv1 = int.from_bytes(response[5:7], 
byteorder='big')  # PV1 power output
                power_output_pv2 = int.from_bytes(response[7:9], 
byteorder='big')  # PV2 power output

                return soc, soh, power_output_pv1, power_output_pv2
            else:
                print('No response from the device.')
                return None

    except serial.SerialException as e:
        print(f'Serial error: {e}')
    except Exception as e:
        print(f'Error: {e}')

# Function to append data to CSV
def append_to_csv(data):
    df = pd.DataFrame(data, columns=['Timestamp', 'SoC', 'SoH', 'Power 
Output PV1', 'Power Output PV2'])
    df.to_csv(CSV_FILE, mode='a', header=not 
pd.io.common.file_exists(CSV_FILE), index=False)

if __name__ == "__main__":
    while True:
        data = read_solar_data()
        if data:
            soc, soh, power_output_pv1, power_output_pv2 = data
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            append_to_csv([(timestamp, soc, soh, power_output_pv1, 
power_output_pv2)])
            print(f'Time: {timestamp}, SoC: {soc}%, SoH: {soh}%, Power 
Output PV1: {power_output_pv1} W, Power Output PV2: {power_output_pv2} W')
        
        time.sleep(10)  # Adjust the sleep interval as needed

