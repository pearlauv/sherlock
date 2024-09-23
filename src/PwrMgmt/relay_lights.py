import RPi.GPIO as GPIO
import schedule
import time
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(filename='/home/pi/Sherlock/data/PwrMgmt/relay_lights.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin connected to the relay
RELAY_PIN = 24  # Using GPIO 24 for this relay

# Setup the GPIO pin as an output
GPIO.setup(RELAY_PIN, GPIO.OUT)

def turn_on():
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    logging.info("Light Relay turned ON")

def turn_off():
    GPIO.output(RELAY_PIN, GPIO.LOW)
    logging.info("Light Relay turned OFF")

def cleanup():
    GPIO.cleanup()
    logging.info("GPIO cleanup complete")

# Schedule the relay operations
schedule.every().day.at("14:15").do(turn_on)  # 6 PM
schedule.every().day.at("15:00").do(turn_off)  # 7 AM

try:
    logging.info("Light Relay control script is running.")
    while True:
        schedule.run_pending()
        time.sleep(1)

except Exception as e:
    logging.error(f"An error occurred: {str(e)}")

finally:
    cleanup()
