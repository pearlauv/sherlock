import csv
import os
from datetime import datetime, timedelta
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
W1_DEVICES_DIR = Path('/sys/bus/w1/devices')
TEMPERATURE_FILE = REPO_ROOT / 'data' / 'Thermal' / 'temperature_readings_by_location.csv'

# Sherlock's DS18B20 sensors all share one 1-Wire data line on BCM GPIO13.
# The Raspberry Pi boot config enables that bus with:
#   dtoverlay=w1-gpio,gpiopin=13
#
# Serial numbers are the Linux 1-Wire device IDs under /sys/bus/w1/devices.
# Leave a serial as None until that physical location is identified.
EXPECTED_SENSORS = [
    {'key': 'h20', 'label': 'H20', 'serial': '28-000000722d76'},
    {'key': 'outside_top', 'label': 'Outside Top', 'serial': '28-0000006a8601'},
    {'key': 'outside_back', 'label': 'Outside Back', 'serial': '28-00000082ff57'},
    {'key': 'inner_middle', 'label': 'Inner Middle', 'serial': '28-0000007c961f'},
    {'key': 'inner_top', 'label': 'Inner Top', 'serial': '28-00000082f49d'},
    {'key': 'inner_bottom', 'label': 'Inner Bottom', 'serial': '28-0000006a25dc'},
]


def load_kernel_modules():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')


def find_detected_serials():
    if not W1_DEVICES_DIR.exists():
        return []

    return sorted(
        device.name
        for device in W1_DEVICES_DIR.glob('28-*')
        if device.is_dir()
    )


def read_temperature(serial):
    device_dir = W1_DEVICES_DIR / serial
    temperature_file = device_dir / 'temperature'
    if not temperature_file.exists():
        return None

    try:
        return float(temperature_file.read_text().strip()) / 1000.0
    except (OSError, ValueError):
        return None


def csv_header():
    return ['Timestamp'] + [sensor['key'] for sensor in EXPECTED_SENSORS]


def ensure_output_file():
    TEMPERATURE_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not TEMPERATURE_FILE.exists() or TEMPERATURE_FILE.stat().st_size == 0:
        with TEMPERATURE_FILE.open(mode='w', newline='') as file:
            csv.writer(file).writerow(csv_header())


def append_reading(row):
    with TEMPERATURE_FILE.open(mode='a', newline='') as file:
        csv.writer(file).writerow(row)


def print_sensor_status(detected_serials):
    configured_serials = {
        sensor['serial']: sensor
        for sensor in EXPECTED_SENSORS
        if sensor['serial'] is not None
    }

    print('\nConfigured sensors:')
    for sensor in EXPECTED_SENSORS:
        serial = sensor['serial'] or 'missing serial'
        present = sensor['serial'] in detected_serials if sensor['serial'] else False
        status = 'detected' if present else 'missing'
        print(f"  {sensor['label']}: {serial} ({status})")

    unmapped_serials = [
        serial
        for serial in detected_serials
        if serial not in configured_serials
    ]
    if unmapped_serials:
        print('\nUnmapped detected sensors:')
        for serial in unmapped_serials:
            print(f'  {serial}')


def collect_reading(timestamp):
    detected_serials = find_detected_serials()
    row = [timestamp]
    readings = []

    for sensor in EXPECTED_SENSORS:
        serial = sensor['serial']
        temperature = read_temperature(serial) if serial in detected_serials else None
        row.append(temperature)
        readings.append((sensor, temperature))

    return detected_serials, readings, row


def seconds_until_next_interval(current_datetime, interval_minutes):
    next_time = (current_datetime + timedelta(minutes=interval_minutes)).replace(
        second=0,
        microsecond=0,
    )
    return (next_time - datetime.now()).total_seconds()


def main():
    load_kernel_modules()
    ensure_output_file()

    print('Starting thermal data logging. Press Ctrl+C to stop.')
    print(f'Writing readings to {TEMPERATURE_FILE}')

    while True:
        current_datetime = datetime.now()
        timestamp = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        detected_serials, readings, row = collect_reading(timestamp)

        print(f'\nTemperatures at {timestamp}:')
        print_sensor_status(detected_serials)
        for sensor, temperature in readings:
            value = '' if temperature is None else f'{temperature:.3f} C'
            print(f"  {sensor['label']}: {value}")

        append_reading(row)

        sleep_duration = seconds_until_next_interval(current_datetime, 15)
        if sleep_duration > 0:
            time.sleep(sleep_duration)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nProgram stopped by user.')
