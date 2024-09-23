import RPi.GPIO as GPIO
import time

# Define GPIO pin where relay is connected
RELAY_PIN = 24  # Example pin number, change to your pin

# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.IN)

# Read the status of the relay pin
relay_status = GPIO.input(RELAY_PIN)

if relay_status == GPIO.HIGH:
    print("Relay is OFF")
else:
    print("Relay is ON")

GPIO.cleanup()
