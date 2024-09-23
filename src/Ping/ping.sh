#!/bin/bash
LOGFILE="/home/pi/Sherlock/data/Ping/ping_log.csv"
HOST="8.8.8.8"

while true; do
    echo "$(date): $(ping -c 1 $HOST | grep 'time=')" >> $LOGFILE
    sleep 30  # Ping every 30 seconds
done
