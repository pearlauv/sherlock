import RPi.GPIO as GPIO
import time

# Set up the GPIO pin
LED_PIN = 24
GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
GPIO.setup(LED_PIN, GPIO.OUT)  # Set pin as an output

try:
    # Turn on the LED
    GPIO.output(LED_PIN, GPIO.HIGH)
    print("LED is ON")
    time.sleep(10)  # Keep it on for 5 seconds

    # Turn off the LED
    GPIO.output(LED_PIN, GPIO.LOW)
    print("LED is OFF")

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()  # Clean up the GPIO settings
