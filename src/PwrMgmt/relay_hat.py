# Keyestudio's relay shield docs list wiringPi pins 7, 3, 22, and 25.
# In the BCM numbering used by RPi.GPIO, those are GPIO4, GPIO22, GPIO6,
# and GPIO26.
KEYESTUDIO_RELAY_CHANNEL_GPIO = {
    1: 4,
    2: 22,
    3: 6,
    4: 26,
}

SHERLOCK_LOAD_RELAY_CHANNEL = {
    'STARLINK': 2,
    'JETSON': 3,
    'LIGHTS': 4,
}


def known_loads():
    return sorted(SHERLOCK_LOAD_RELAY_CHANNEL)


def relay_channel_for_load(load_name):
    """Resolve a Sherlock load name to the physical relay channel."""
    load_key = load_name.upper()

    try:
        return SHERLOCK_LOAD_RELAY_CHANNEL[load_key]
    except KeyError as exc:
        loads = ", ".join(known_loads())
        raise RuntimeError(f"Unknown Sherlock relay load {load_name!r}. Known loads: {loads}.") from exc


def relay_pin_for_load(load_name):
    """Resolve a Sherlock load name to the BCM GPIO used by the relay HAT."""
    channel = relay_channel_for_load(load_name)

    return KEYESTUDIO_RELAY_CHANNEL_GPIO[channel]
