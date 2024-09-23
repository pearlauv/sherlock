import RPi.GPIO as GPIO
import time

# Define GPIO pin where relay is connected
RELAY_PIN = 24  # Example pin number, change to your pin

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

# Function to toggle relay
def toggle_relay():
    # Turn relay ON
    GPIO.output(RELAY_PIN, GPIO.LOW)  # Assuming active-low relay
    print("Relay is ON")
    time.sleep(2)  # Keep relay on for 2 seconds
    
    # Turn relay OFF
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    print("Relay is OFF")
    time.sleep(2)  # Keep relay off for 2 seconds

try:
    # Toggle relay a few times
    for _ in range(5):
        toggle_relay()

finally:
    GPIO.cleanup()
