# Sherlock 1-Wire Thermal Sensors

Sherlock uses DS18B20-style 1-Wire temperature sensors. All sensors share one
data wire on BCM GPIO13. The Raspberry Pi boot config must contain:

```ini
dtoverlay=w1-gpio,gpiopin=13
```

The rigging image build configures this in Ansible. On a live Pi, verify it with:

```bash
grep -nE '^(enable_uart|dtoverlay=w1)' /boot/firmware/config.txt
```

After boot, detected sensors appear under:

```bash
/sys/bus/w1/devices/
```

Valid DS18B20 device IDs start with `28-`:

```bash
find /sys/bus/w1/devices -maxdepth 1 -mindepth 1 -name '28-*' -printf '%f\n' | sort
```

The current Sherlock mapping in `brain_temp.py` is:

| Location | Serial |
| --- | --- |
| H20 | `28-000000722d76` |
| Outside Top | `28-0000006a8601` |
| Outside Back | `28-00000082ff57` |
| Inner Middle | `28-0000007c961f` - right back connection presently |
| Inner Top | `28-00000082f49d` - middle back connection presently |
| Inner Bottom | `28-0000006a25dc` - left back connection presently |

Raspberry Pi OS exposes a direct milli-Celsius temperature file for each sensor:

```bash
cat /sys/bus/w1/devices/28-0000006a8601/temperature
```

For example, `21437` means `21.437 C`.

The older `w1_slave` file is still useful for manual diagnostics because it
includes CRC status:

```bash
cat /sys/bus/w1/devices/28-0000006a8601/w1_slave
```

A valid reading looks like:

```text
6b 01 4b 46 7f ff 0c 10 8b : crc=8b YES
6b 01 4b 46 7f ff 0c 10 8b t=22375
```

The `brain_temp.py` logger reads the direct `temperature` file and writes stable
physical-location columns to:

```text
data/Thermal/temperature_readings_by_location.csv
```
