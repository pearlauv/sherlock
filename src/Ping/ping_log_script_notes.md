# Notes on Ping Log Shell Script

## Overview
This shell script is designed to continuously ping a set of predefined hosts and log the response times to a CSV file. It runs indefinitely, capturing network performance at regular intervals.

## Script Breakdown

### Variables
- **LOGFILE**: This variable specifies the path to the CSV file where the ping results will be logged. In this case, it's set to `/home/pi/Sherlock/data/Ping/ping_log.csv`.
  
- **HOST1 to HOST5**: These variables represent different IP addresses of the hosts being pinged:
  - **HOST1**: `8.8.8.8` (Google's public DNS server)
  - **HOST2**: `10.49.0.1` (ServerPi)
  - **HOST3**: `10.49.0.2` (Oyster)
  - **HOST4**: `10.49.0.4` (NavPi)
  - **HOST5**: `10.49.0.9` (PantherPi)

### Main Loop
The script enters an infinite `while` loop, which allows it to continuously execute the commands within it:

1. **Date and Ping Command**: For each host, the script performs the following:
   - Uses the `date` command to get the current date and time.
   - Executes the `ping` command with `-c 1` to send a single ping packet.
   - Uses `grep 'time='` to filter the output and retrieve the round-trip time.
   
2. **Logging**: The results are appended to the specified log file. Each entry includes:
   - The date and time of the ping attempt.
   - The host identifier (e.g., Google, ServerPi) followed by the response time.

3. **Sleep Interval**: After pinging all hosts, the script pauses for 30 seconds using `sleep 30`, allowing for periodic checks without overwhelming the network.

### Usage
- **Running the Script**: This script can be run in a terminal session on a Raspberry Pi or other compatible Linux environment. Make sure the script has execute permissions (`chmod +x ping.sh`).
  
- **Executing with Screen**:
  1. Start a new screen session:
     ```bash
     screen
     ```
  2. Run the script:
     ```bash
     ./ping.sh
     ```
  3. To detach from the screen session and leave the script running in the background, press `Ctrl + A`, then `D`.
  4. To list all active screen sessions, use:
     ```bash
     screen -ls
     ```
  5. To reattach to a specific session, use:
     ```bash
     screen -r <session_id>
     ```
     Replace `<session_id>` with the actual session ID listed in the output from `screen -ls`.

- **Stopping the Script**: If you need to stop the script, reattach to the screen session and press `Ctrl + C`.

### Important Considerations
- **Permissions**: Ensure the script has the necessary permissions to write to the specified log file.
  
- **Log File Management**: The log file will grow indefinitely; consider implementing log rotation or periodic cleanup to manage file size.

- **Network Configuration**: The host IPs must be reachable from the device running the script. Adjust the IP addresses as necessary based on your network configuration.

## Conclusion
This script is a simple yet effective way to monitor network latency to specific hosts over time. It can be used for troubleshooting network issues or ensuring connectivity to critical devices within a network.
