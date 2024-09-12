# Open raspi-config to enable the 1-Wire interface
sudo raspi-config

# Navigate through the menu:
# - Select "Interface Options"
# - Choose "1-Wire"
# - Enable the 1-Wire interface
# - Finish and reboot the Raspberry Pi when prompted

# After rebooting, open the config.txt file for editing
sudo nano /boot/firmware/config.txt

# Inside the nano editor, add the following line to the end of the file
dtoverlay=w1-gpio,gpiopin=22
# Save and exit the editor:
# - Press Ctrl+X to exit
# - Press Y to confirm saving changes
# - Press Enter to save the file

# Reboot the Raspberry Pi to apply the changes
sudo reboot

# After rebooting, check if the 1-Wire devices are detected
# List the contents of the /sys/bus/w1/devices/ directory
ls /sys/bus/w1/devices/

# Example output might include directories like:
# 28-000005e2fdc3
# 28-000005e2fdc4

# To verify the sensor data, check the contents of one of the device files
# Replace 28-000005e2fdc3 with your actual device ID
cat /sys/bus/w1/devices/28-000005e2fdc3/w1_slave

# Example output might include lines like:
# 6b 01 4b 46 7f ff 0c 10 8b : crc=8b YES
# 6b 01 4b 46 7f ff 0c 10 8b t=22375

# The t=22375 part represents the temperature in thousandths of a degree Celsius (22.375°C)
