import RPi.GPIO as GPIO
import time
from datetime import datetime

# Set up GPIO
GPIO.setmode(GPIO.BCM)
relay_pin = 17  # Change this to your GPIO pin
GPIO.setup(relay_pin, GPIO.OUT, initial=GPIO.LOW)

def main():
    # Define start and end times
    start_times = [(10, 0), (16, 0)]  # List of start times (hour, minute)
    end_times = [(10, 30), (16, 30)]    # List of end times (hour, minute)

    while True:
        now = datetime.now()
        current_hour = now.hour
        current_minute = now.minute

        relay_on = False

        # Check if current time is within any of the start and end intervals
        for (start_hour, start_minute), (end_hour, end_minute) in zip(start_times, end_times):
            if (current_hour > start_hour or (current_hour == start_hour and current_minute >= start_minute)) and \
               (current_hour < end_hour or (current_hour == end_hour and current_minute <= end_minute)):
                relay_on = True
                break

        # Set relay state based on the above condition
        if relay_on:
            GPIO.output(relay_pin, GPIO.HIGH)  # Turn on relay
        else:
            GPIO.output(relay_pin, GPIO.LOW)  # Turn off relay

        time.sleep(30)  # Check every 30 seconds to be more responsive

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Program interrupted and GPIO cleaned up.")
