#!/usr/bin/env python3
import argparse
import grp
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

from relay_hat import known_loads, relay_channel_for_load, relay_pin_for_load


# The current Sherlock relay HAT wiring is active-high:
# driving high energizes the relay, driving low de-energizes it.
RELAY_STATE = {
    'on': '1',
    'off': '0',
}

GPIO_CHIP = 'gpiochip0'
PID_DIR = Path('/tmp/sherlock-relay-control')


def can_run_gpio_tools_directly():
    if os.geteuid() == 0:
        return True

    try:
        gpio_gid = grp.getgrnam('gpio').gr_gid
    except KeyError:
        return False

    return gpio_gid in os.getgroups()


def with_gpio_permissions(command):
    if can_run_gpio_tools_directly():
        return command

    if shutil.which('sudo') is None:
        sys.exit('Run this command as root or add the user to the gpio group.')

    return ['sudo', '-n', *command]


def holder_consumer(load):
    return f'sherlock-relay-{load.lower()}'


def holder_pid_path(load):
    return PID_DIR / f'{load.lower()}.pid'


def process_command(pid):
    try:
        return Path(f'/proc/{pid}/cmdline').read_bytes().replace(b'\0', b' ').decode()
    except OSError:
        return ''


def find_holder_pids(consumer):
    pids = []

    for proc_dir in Path('/proc').iterdir():
        if not proc_dir.name.isdigit():
            continue

        try:
            if (proc_dir / 'comm').read_text().strip() != 'gpioset':
                continue
        except OSError:
            continue

        if consumer in process_command(proc_dir.name):
            pids.append(int(proc_dir.name))

    return pids


def kill_process(pid):
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    except PermissionError:
        subprocess.run(with_gpio_permissions(['kill', str(pid)]), check=True)


def stop_existing_holder(load, consumer):
    pid_path = holder_pid_path(load)
    pids = set(find_holder_pids(consumer))

    try:
        pids.add(int(pid_path.read_text().strip()))
    except (OSError, ValueError):
        pass

    for pid in pids:
        kill_process(pid)

    deadline = time.monotonic() + 2
    while time.monotonic() < deadline:
        if not any(Path(f'/proc/{pid}').exists() for pid in pids):
            break
        time.sleep(0.05)

    try:
        pid_path.unlink()
    except FileNotFoundError:
        pass


def start_holder(load, consumer, pin, state):
    command = [
        'gpioset',
        '-z',
        '-c',
        GPIO_CHIP,
        '-C',
        consumer,
        f'{pin}={RELAY_STATE[state]}',
    ]

    if shutil.which(command[0]) is None:
        sys.exit('gpioset is required for persistent relay control on this Raspberry Pi.')

    subprocess.run(with_gpio_permissions(command), check=True)

    pids = find_holder_pids(consumer)
    if not pids:
        sys.exit(f'Failed to confirm persistent gpioset holder for {load}.')

    PID_DIR.mkdir(parents=True, exist_ok=True)
    holder_pid_path(load).write_text(f'{pids[-1]}\n')


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


def set_relay(load_name, state):
    load = load_name.upper()
    channel = relay_channel_for_load(load)
    pin = relay_pin_for_load(load)

    consumer = holder_consumer(load)
    stop_existing_holder(load, consumer)
    start_holder(load, consumer, pin, state)

    return load, channel, pin


def main():
    args = parse_args()
    load, channel, pin = set_relay(args.load, args.state)

    print(f'{load} {args.state.upper()} via relay CH{channel} / GPIO{pin}')


if __name__ == '__main__':
    main()
