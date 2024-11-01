# Network-Auditor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python script designed to simplify network troubleshooting and auditing for system administrators, security professionals, and network engineers on Linux systems. Network-Auditor streamlines the process by providing a single, unified view of key network configurations in an easy-to-read, color-coded format.

## Features

* **List Network Interfaces:** Displays all network interfaces and their statuses (up/down).
* **Show IP Addresses:** Shows IP addresses assigned to each interface.
* **Show Routing Table:** Displays the current routing table.
* **Show Firewall Rules:** Shows the current UFW (Uncomplicated Firewall) rules. Requires `sudo` access.
* **List Open Connections:** Lists open network connections.
* **List Docker Networks:** Lists Docker networks and their connected containers with IP addresses (requires Docker).
* **Run All Checks:** Performs all of the above checks in sequence.
* **Interactive Menu:** Provides a user-friendly menu for easy navigation.
* **Color-Coded Output:** Enhances readability and highlights important information.
* **Logging:** Records all actions and errors in `audit_network.log` for auditing and debugging.
* **Command-line option:** Run all checks non-interactively with `--all`.

## Prerequisites

* **Python 3.x:** Ensure Python 3.x is installed.
* **Tabulate Library:** Install using: `pip install tabulate`
* **Required System Commands:** `ip`, `ss`, `ufw` (for firewall rules), `docker` (for Docker network listing).

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/elliotsecops/Network-Auditor.git
   cd Network-Auditor
   ```

2. **Install Required Packages:**
   ```bash
   pip install tabulate
   ```

## Usage

1. **Interactive Mode:**
   ```bash
   python3 network_audit.py 
   ```
   Follow the on-screen menu to select the desired checks.

2. **Run All Checks (Non-Interactive):**
   ```bash
   sudo python3 network_audit.py --all  # Recommended to run with sudo for full functionality
   ```
   or
   ```bash
   python3 network_audit.py --all # Some features won't work
   ```

## Security Considerations

Network-Auditor requires superuser privileges (`sudo`) for certain checks, like viewing firewall rules. It is recommended to run the entire script using `sudo` for complete functionality. If you choose to run without `sudo`, some features will not work correctly. If you run it interactively, the script will prompt you for your password when elevated privileges are required. Use `sudo` judiciously and be aware of the potential security implications of running scripts with elevated privileges.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests for bug reports, feature requests, or other improvements. For detailed guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Acknowledgments

* The `tabulate` library for creating formatted tables.

## Contact
elliotsecops@proton.me
