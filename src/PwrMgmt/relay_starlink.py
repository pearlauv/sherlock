import schedule
import time
import logging
from datetime import datetime
from pathlib import Path

from relay_control import set_relay

REPO_ROOT = Path(__file__).resolve().parents[2]

# Set up logging
logging.basicConfig(
    filename=REPO_ROOT / 'data' / 'PwrMgmt' / 'relay_starlink.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def turn_on():
    set_relay('STARLINK', 'on')
    logging.info("Starlink Relay turned ON")

def turn_off():
    set_relay('STARLINK', 'off')
    logging.info("Starlink Relay turned OFF")

# Without this, startup within window wouldn't guarantee starlink turns on
def set_initial_state():
    now = datetime.now().time()
    windows = [
        ("10:00", "10:30"),
        ("16:00", "16:30"),
    ]

    active = any(
        datetime.strptime(start, "%H:%M").time() <= now < datetime.strptime(end, "%H:%M").time()
        for start, end in windows
    )

    if active:
        turn_on()
    else:
        turn_off()

# Schedule the relay operations
schedule.every().day.at("10:00").do(turn_on)
schedule.every().day.at("10:30").do(turn_off)
schedule.every().day.at("16:00").do(turn_on)
schedule.every().day.at("16:30").do(turn_off)

try:
    logging.info("Starlink Relay control script is running.")
    set_initial_state()
    while True:
        schedule.run_pending()
        time.sleep(1)

except Exception as e:
    logging.error(f"An error occurred: {str(e)}")

finally:
    logging.info("Starlink Relay control script stopped.")
