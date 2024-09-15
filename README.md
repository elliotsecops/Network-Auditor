
# Network Configuration Audit Tool

## Overview

The Network Configuration Audit Tool is a Python script designed to audit and report system network configurations on Linux systems. It provides a comprehensive overview of active network interfaces, IP addresses, routing tables, firewall rules (UFW), and open network connections. The tool is particularly useful for system administrators and network professionals who need to quickly check various aspects of their network setup.

## Features

- **Network Interfaces**: Lists all network interfaces and their status (active/inactive).
- **IP Addresses**: Displays the IP addresses assigned to each network interface.
- **Routing Table**: Shows the current routing table.
- **Firewall Rules**: Displays the first firewall rules (UFW).
- **Open Connections**: Lists some of the open network connections.
- **Interactive Menu**: Provides an interactive menu for easy navigation and selection of specific checks.
- **Color-Coded Output**: Enhances readability by highlighting important information.
- **Logging**: Logs all actions and errors to `audit_network.log` for auditing and debugging purposes.

## Prerequisites

- **Python 3.x**: Ensure Python 3.x is installed on your system.
- **Tabulate Library**: Install the `tabulate` library using pip:
  ```bash
  pip install tabulate
  ```
- **System Commands**: The script requires the following commands to be available on your system:
  - `ip`
  - `ss`
  - `ufw` (for firewall rules)

## Installation

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/elliotsecops/network-configuration-audit.git
   cd network-configuration-audit
   ```

2. Install the required Python package:
   ```bash
   pip install tabulate
   ```

## Usage

1. Run the script with superuser permissions:
   ```bash
   sudo python3 network_audit.py
   ```

2. The script will present an interactive menu. Choose the desired option to perform specific checks or run all checks sequentially.

### Example Output

```
Network Configuration Audit

Network Configuration Audit Menu:
1. List network interfaces
2. Show IP addresses
3. Show routing table
4. Show firewall rules
5. List open network connections
6. Run all checks
7. Exit

Enter your choice: 6

Network interfaces and their status:
+--------------+--------+
| Interface    | Status |
+--------------+--------+
| lo           | UP     |
| eth0         | UP     |
| wlan0        | DOWN   |
+--------------+--------+

IP addresses assigned to each interface:
+--------------+----------------+
| Interface    | IP Address     |
+--------------+----------------+
| lo           | 127.0.0.1/8    |
| eth0         | 192.168.1.2/24 |
+--------------+----------------+

Current routing table:
+------------------------------------------------------------------------+
| Route                                                                  |
+------------------------------------------------------------------------+
| default via 192.168.1.1 dev eth0                                       |
| 192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.2       |
| 127.0.0.0/8 dev lo proto kernel scope link src 127.0.0.1              |
+------------------------------------------------------------------------+

First firewall (UFW) rules:
+----------------------------------------+
| UFW Rule                               |
+----------------------------------------+
| [ 1] 22/tcp (v6) ALLOW IN Anywhere (v6)|
| [ 2] 80/tcp (v6) ALLOW IN Anywhere (v6)|
+----------------------------------------+

Some open network connections:
+--------+-------------------+-------------------+
| State  | Local Address     | Remote Address    |
+--------+-------------------+-------------------+
| LISTEN | 0.0.0.0:22        | 0.0.0.0:*         |
| LISTEN | 0.0.0.0:80        | 0.0.0.0:*         |
+--------+-------------------+-------------------+

Exiting. Thank you for using the Network Configuration Audit tool.
```

## Logging

All actions and errors are logged to `audit_network.log`. This file can be useful for auditing and debugging purposes.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

