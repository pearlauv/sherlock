import RPi.GPIO as GPIO
import time
from datetime import datetime

# Set up GPIO
GPIO.setmode(GPIO.BCM)
relay_pin = 17  # Change this to your GPIO pin
GPIO.setup(relay_pin, GPIO.OUT, initial=GPIO.LOW)

def main():
    start_hour = 14  # 5:00 PM
    start_minute = 0
    end_hour = 14    # 6:00 PM
    end_minute = 30

    while True:
        now = datetime.now()
        current_hour = now.hour
        current_minute = now.minute

        if current_hour == start_hour and current_minute == start_minute:
            GPIO.output(relay_pin, GPIO.HIGH)  # Turn on relay
        elif current_hour == end_hour and current_minute == end_minute:
            GPIO.output(relay_pin, GPIO.LOW)  # Turn off relay

        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
