#!/usr/bin/env python3
import argparse

import RPi.GPIO as GPIO

from relay_hat import known_loads, relay_channel_for_load, relay_pin_for_load


# The current Sherlock relay HAT wiring is active-high:
# GPIO.HIGH energizes the relay, GPIO.LOW de-energizes it.
RELAY_STATE = {
    'on': GPIO.HIGH,
    'off': GPIO.LOW,
}


def parse_args():
    parser = argparse.ArgumentParser(
        description='Manually switch a Sherlock relay-controlled load.',
    )
    parser.add_argument(
        'load',
        choices=[load.lower() for load in known_loads()],
        help='Load to switch.',
    )
    parser.add_argument(
        'state',
        choices=sorted(RELAY_STATE),
        help='Desired relay state.',
    )
    return parser.parse_args()


def main():
    args = parse_args()
    load = args.load.upper()
    channel = relay_channel_for_load(load)
    pin = relay_pin_for_load(load)

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, RELAY_STATE[args.state])

    print(f'{load} {args.state.upper()} via relay CH{channel} / GPIO{pin}')


if __name__ == '__main__':
    main()
