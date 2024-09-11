import asyncio
import time
import os
from bleak import BleakClient
from datetime import datetime

# Replace with CMPower battery's MAC address
BATTERY_MAC = "<MAC address>"

# Replace with correct UUIDs for SOC and SOH from CMPower
SOC_UUID = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
SOH_UUID = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"

# Path to the CSV file
CSV_FILE_PATH = "battery_data.csv"

async def monitor_battery():
    async with BleakClient(BATTERY_MAC) as client:
        # Check if the file exists and write header if it doesn't
        if not os.path.isfile(CSV_FILE_PATH):
            with open(CSV_FILE_PATH, "w") as f:
                f.write("datetime,soc,soh\n")

        while True:
            try:
                # Get SOC and SOH data
                soc_data = await client.read_gatt_char(SOC_UUID)
                soh_data = await client.read_gatt_char(SOH_UUID)

                # Convert to integer values
                soc = int.from_bytes(soc_data, byteorder="little")
                soh = int.from_bytes(soh_data, byteorder="little")

                # Get the current date and time
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Print to console (optional)
                print(f"{current_time} - SOC: {soc}%, SOH: {soh}%")

                # Append data to the CSV file with timestamp
                with open(CSV_FILE_PATH, "a") as f:
                    f.write(f"{current_time},{soc},{soh}\n")

                # Wait for 15 minutes before the next sample
                time.sleep(900)  # 900 seconds = 15 minutes

            except Exception as e:
                print(f"Error occurred: {e}")
                break

# Run the monitoring function
loop = asyncio.get_event_loop()
loop.run_until_complete(monitor_battery())
