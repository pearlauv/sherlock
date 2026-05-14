import RPi.GPIO as GPIO
import schedule
import time
import logging
from datetime import datetime
from pathlib import Path

from relay_hat import relay_pin_for_load

REPO_ROOT = Path(__file__).resolve().parents[2]

# Set up logging
logging.basicConfig(
    filename=REPO_ROOT / 'data' / 'PwrMgmt' / 'relay_lights.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Resolve CH4 to the BCM GPIO used by the Keyestudio relay HAT.
RELAY_PIN = relay_pin_for_load('LIGHTS')

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

# Without this, startup within the 'on' window wouldn't guarantee lights on
def set_initial_state():
    now = datetime.now().time()
    on_time = datetime.strptime("18:00", "%H:%M").time()
    off_time = datetime.strptime("07:00", "%H:%M").time()

    if now >= on_time or now < off_time:
        turn_on()
    else:
        turn_off()

# Schedule the relay operations
schedule.every().day.at("18:00").do(turn_on)  # 6 PM
schedule.every().day.at("07:00").do(turn_off)  # 7 AM

try:
    logging.info("Light Relay control script is running.")
    set_initial_state()
    while True:
        schedule.run_pending()
        time.sleep(1)

except Exception as e:
    logging.error(f"An error occurred: {str(e)}")

finally:
    cleanup()
