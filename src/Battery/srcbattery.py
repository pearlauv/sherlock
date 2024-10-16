import serial
import time

#GPIO14 -- PIN 8  -- UART TX
#GPIO15 -- PIN 10 -- UART RX

# Initialize the serial connection to the ESP32
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Replace ttyS0 with your serial port
time.sleep(2)  # Give the serial connection some time to initialize

def read_battery_data():
    # Request data from the ESP32
    ser.write(b'REQUEST\n')  # Send a request command to the ESP32

    # Read data from the ESP32
    line = ser.readline().decode('utf-8').strip()
    
    # If data received, process it
    if line:
        try:
            # Expecting data in format: "Voltage:12.6,Current:1.2,Power:15.1,SoC:75,SoH:100"
            data = line.split(',')
            battery_data = {}
            for item in data:
                key, value = item.split(':')
                battery_data[key.strip()] = float(value.strip())
            return battery_data
        except Exception as e:
            print(f"Error processing data: {e}")
            return None
    return None

def main():
    while True:
        battery_data = read_battery_data()

        if battery_data:
            # Display the battery data
            print(f"Voltage: {battery_data['Voltage']} V")
            print(f"Current: {battery_data['Current']} A")
            print(f"Power: {battery_data['Power']} W")
            print(f"State of Charge (SoC): {battery_data['SoC']}%")
            print(f"State of Health (SoH): {battery_data['SoH']}%")
            print("-----------------------------")

        # Wait before requesting the next data point
        time.sleep(2)

if __name__ == "__main__":
    main()
