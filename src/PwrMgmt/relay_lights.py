import schedule
import time
import logging
from datetime import datetime
from pathlib import Path

from relay_control import set_relay

REPO_ROOT = Path(__file__).resolve().parents[2]

# Set up logging
logging.basicConfig(
    filename=REPO_ROOT / 'data' / 'PwrMgmt' / 'relay_lights.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def turn_on():
    set_relay('LIGHTS', 'on')
    logging.info("Light Relay turned ON")

def turn_off():
    set_relay('LIGHTS', 'off')
    logging.info("Light Relay turned OFF")

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
    logging.info("Light Relay control script stopped.")
