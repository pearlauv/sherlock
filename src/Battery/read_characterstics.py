import asyncio
from bleak import BleakClient

# Replace with your device's MAC address
BATTERY_MAC = "31:38:05:00:4D:7F"

# List of UUIDs you want to check (add more if needed)
uuids = [
    "0000180a-0000-1000-8000-00805f9b34fb",
    "0000fd00-0000-1000-8000-00805f9b34fb",
    "0000ff90-0000-1000-8000-00805f9b34fb",
    "0000ffb0-0000-1000-8000-00805f9b34fb",
    "0000ffc0-0000-1000-8000-00805f9b34fb",
    "0000ffd0-0000-1000-8000-00805f9b34fb",
    "0000fff0-0000-1000-8000-00805f9b34fb",
    "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
]

async def read_characteristics():
    async with BleakClient(BATTERY_MAC) as client:
        for uuid in uuids:
            try:
                data = await client.read_gatt_char(uuid)
                # Interpret the data as needed (e.g., as an integer)
                value = int.from_bytes(data, byteorder="little")
                print(f"UUID: {uuid} -> Value: {value}")
            except Exception as e:
                print(f"Could not read from {uuid}: {e}")

# Run the async function
loop = asyncio.get_event_loop()
loop.run_until_complete(read_characteristics())
