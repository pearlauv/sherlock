import RPi.GPIO as GPIO
import time

# Set up the GPIO pin
RELAY_PIN = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

try:
    while True:
        # Turn the relay on
        GPIO.output(RELAY_PIN, GPIO.HIGH)
        print("Relay is ON")
        #time.sleep(1)

        # Turn the relay off
        #GPIO.output(RELAY_PIN, GPIO.LOW)
        #print("Relay is OFF")
        #time.sleep(1)

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
