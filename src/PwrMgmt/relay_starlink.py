import RPi.GPIO as GPIO
import schedule
import time
from datetime import datetime
import logging

# Set up logging
<<<<<<< HEAD
logging.basicConfig(filename='/home/pi/Sherlock/data/PwrMgmt/relay_starlink.log', level=logging.INFO, 
=======
logging.basicConfig(filename='/home/pi/Sherlock/data/PwrMgmt/relay_control.log', level=logging.INFO, 
>>>>>>> b9b4f017998081a666be76460e3d531ce2d658c3
                    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin connected to the relay
RELAY_PIN = 23

# Setup the GPIO pin as an output
GPIO.setup(RELAY_PIN, GPIO.OUT)

def turn_on():
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    logging.info("Relay turned ON")

def turn_off():
    GPIO.output(RELAY_PIN, GPIO.LOW)
    logging.info("Relay turned OFF")

def cleanup():
    GPIO.cleanup()
    logging.info("GPIO cleanup complete")

# Schedule the relay operations
<<<<<<< HEAD
schedule.every().day.at("14:15").do(turn_on)
schedule.every().day.at("14:45").do(turn_off)
=======
schedule.every().day.at("10:00").do(turn_on)
schedule.every().day.at("10:30").do(turn_off)
>>>>>>> b9b4f017998081a666be76460e3d531ce2d658c3
schedule.every().day.at("16:00").do(turn_on)
schedule.every().day.at("16:30").do(turn_off)

try:
<<<<<<< HEAD
    logging.info("Starlink Relay control script is running.")
=======
    logging.info("Relay control script is running.")
>>>>>>> b9b4f017998081a666be76460e3d531ce2d658c3
    while True:
        schedule.run_pending()
        time.sleep(1)

except Exception as e:
    logging.error(f"An error occurred: {str(e)}")

finally:
<<<<<<< HEAD
    cleanup()
=======
    cleanup()
>>>>>>> b9b4f017998081a666be76460e3d531ce2d658c3
