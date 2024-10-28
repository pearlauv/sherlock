import RPi.GPIO as GPIO
import schedule
import time
import logging

# Set up logging
logging.basicConfig(
    filename='/home/pi/sherlock/data/PwrMgmt/relay_starlink.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin connected to the relay
RELAY_PIN = 25

# Setup the GPIO pin as an output
GPIO.setup(RELAY_PIN, GPIO.OUT)

def turn_on():
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    logging.info("Starlink Relay turned ON")

def turn_off():
    GPIO.output(RELAY_PIN, GPIO.LOW)
    logging.info("Starlink Relay turned OFF")

def cleanup():
    GPIO.cleanup()
    logging.info("GPIO cleanup complete")

# Schedule the relay operations
schedule.every().day.at("10:00").do(turn_on)
schedule.every().day.at("10:30").do(turn_off)
schedule.every().day.at("16:00").do(turn_on)
schedule.every().day.at("16:30").do(turn_off)

try:
    logging.info("Starlink Relay control script is running.")
    while True:
        schedule.run_pending()
        time.sleep(1)

except Exception as e:
    logging.error(f"An error occurred: {str(e)}")

finally:
    cleanup()
