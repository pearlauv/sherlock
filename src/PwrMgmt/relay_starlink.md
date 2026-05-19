# Raspberry Pi Starlink Relay Control Script

This document outlines how to control a relay connected to a Raspberry Pi for managing a Starlink connection using a Python script. The script automatically manages the relay state based on a schedule and logs its activities.

## Overview of the Code

### Libraries Used

- **RPi.GPIO**: For controlling GPIO pins.
- **schedule**: For scheduling tasks.
- **time**: For time-related functions.
- **logging**: For logging events to a file.

### Key Components

1. **Logging Setup**: 
   - Logs are stored at `data/PwrMgmt/relay_starlink.log` under the Sherlock repo checkout.
   - Log entries include timestamps and messages.

2. **GPIO Setup**:
   - The GPIO mode is set to BCM.
   - The Keyestudio relay HAT uses BCM GPIO4, GPIO22, GPIO6, and GPIO26
     for relay channels 1-4.
   - Starlink is wired to relay channel 2, which maps to BCM GPIO22.

3. **Relay Control Functions**:
   - `turn_on()`: Activates the relay and logs the action.
   - `turn_off()`: Deactivates the relay and logs the action.
   - `cleanup()`: Cleans up GPIO settings and logs the cleanup.

4. **Scheduling**:
   - The relay turns on at 10:00 AM and 4:00 PM, and turns off at 10:30 AM and 4:30 PM daily using the `schedule` library.

5. **Main Loop**:
   - A while loop runs indefinitely, executing scheduled tasks every second.
   - Exceptions are logged, and cleanup is performed on exit.

## How to Execute the Script

### Prerequisites

Make sure you have Python and the necessary libraries installed:

```bash
sudo apt-get update
sudo apt-get install python3 python3-rpi.gpio python3-schedule gpiod
```

### Running the Script

You can run the script directly from the terminal with:

```bash
python3 /home/sherlock/sherlock/src/PwrMgmt/relay_starlink.py
```

To manually switch the Starlink relay without starting the scheduler:

```bash
python3 /home/sherlock/sherlock/src/PwrMgmt/relay_control.py starlink on
python3 /home/sherlock/sherlock/src/PwrMgmt/relay_control.py starlink off
```

The manual control helper uses `gpioset` to keep the relay GPIO held after the
command exits. Running either command again for the same load replaces the
previous holder process.

### Setting Up as a Service

To run the script as a service, follow these steps:

1. **Create a Service File**:

   Open a new service file for the relay control script:

   ```bash
   sudo nano /etc/systemd/system/relay_starlink.service
   ```

2. **Add the Service Configuration**:

   Use the following configuration:

   ```ini
   [Unit]
   Description=Relay Control Service
   After=multi-user.target

   [Service]
   ExecStart=/usr/bin/python3 /home/sherlock/sherlock/src/PwrMgmt/relay_starlink.py
   WorkingDirectory=/home/sherlock/sherlock/src/PwrMgmt
   StandardOutput=inherit
   StandardError=inherit
   Restart=always
   User=sherlock

   [Install]
   WantedBy=multi-user.target
   ```

3. **Enable and Start the Service**:

   Reload the systemd manager configuration, enable the service, and start it:

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable relay_starlink.service
   sudo systemctl start relay_starlink.service
   ```

4. **Check Service Status**:

   Verify that the service is running with:

   ```bash
   sudo systemctl status relay_starlink.service
   ```

## Conclusion

This script effectively manages a relay for Starlink control based on a set schedule while logging its operations. Running it as a service ensures that it operates in the background, starting automatically with your Raspberry Pi.
