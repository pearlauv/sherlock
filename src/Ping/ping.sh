#!/bin/bash
LOGFILE="/home/pi/Sherlock/data/Ping/ping_log.csv"
HOST1="8.8.8.8"
HOST2="10.49.0.2"
HOST3="10.49.0.4"
HOST4="10.49.0.9"
while true; do
    echo "$(date): Google       $(ping -c 1 $HOST1 | grep 'time=')" >> $LOGFILE
    echo "$(date): Oyster       $(ping -c 1 $HOST2 | grep 'time=')" >> $LOGFILE
    echo "$(date): NavPi        $(ping -c 1 $HOST3 | grep 'time=')" >> $LOGFILE
    echo "$(date): PantherPi    $(ping -c 1 $HOST4 | grep 'time=')" >> $LOGFILE
    sleep 30  # Ping every 30 seconds
done
