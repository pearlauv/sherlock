import serial
import time

# Replace '/dev/ttyUSB0' with your actual USB device path
ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=1)

def read_ping():
    ser.write(b'R')  # Send the request to read
    time.sleep(0.1)  # Allow some time for the sensor to respond
    if ser.in_waiting > 0:
        distance = ser.readline().decode('utf-8').strip() * 0.01
        return distance
    return None

try:
    while True:
        distance = read_ping()
        if distance is not None:
            print(f"Distance: {distance} m")
        time.sleep(1)

except KeyboardInterrupt:
    print("Program stopped.")

finally:
    ser.close()

