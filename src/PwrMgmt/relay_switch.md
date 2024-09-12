# Step 1: Save your Python script
sudo mkdir -p /home/pi/Sherlock/src/PwrMgmt
sudo nano /home/pi/Sherlock/src/PwrMgmt/relay_switch.py

# Paste the following Python script into the editor:
# (Use Ctrl+Shift+V to paste or right-click and paste)
"""
import RPi.GPIO as GPIO
import time
from datetime import datetime

# Set up GPIO
GPIO.setmode(GPIO.BCM)
relay_pin = 17  # Change this to your GPIO pin
GPIO.setup(relay_pin, GPIO.OUT, initial=GPIO.LOW)

def main():
    # Define start and end times
    start_times = [(14, 0), (18, 0)]  # List of start times (hour, minute)
    end_times = [(15, 0), (20, 0)]    # List of end times (hour, minute)

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
"""
# Save and exit nano: Ctrl+X, Y, Enter

# Make the script executable
sudo chmod +x /home/pi/Sherlock/src/PwrMgmt/relay_switch.py

# Step 2: Create the systemd service file
sudo nano /etc/systemd/system/relay_switch.service

# Paste the following service configuration into the editor:
# (Use Ctrl+Shift+V to paste or right-click and paste)
"""
[Unit]
Description=Relay Switch Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/Sherlock/src/PwrMgmt/relay_switch.py
WorkingDirectory=/home/pi/Sherlock/src/PwrMgmt
Restart=always
User=pi
Group=pi

[Install]
WantedBy=multi-user.target
"""
# Save and exit nano: Ctrl+X, Y, Enter

# Step 3: Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable relay_switch.service
sudo systemctl start relay_switch.service

# Step 4: Check the status of the service
sudo systemctl status relay_switch.service

# Optional: View logs for the service
journalctl -u relay_switch.service
