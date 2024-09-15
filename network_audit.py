import subprocess
import logging
from tabulate import tabulate

# Configure logging
logging.basicConfig(filename='audit_network.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
NC = '\033[0m'  # No Color

def execute_command(command):
    try:
        result = subprocess.run(command, shell=False, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        error_msg = f"Error executing {' '.join(command)}: {e.stderr}"
        logging.error(error_msg)
        return error_msg

def list_interfaces():
    print(f"\n{BLUE}Network interfaces and their status:{NC}")
    interfaces = execute_command(["ip", "-br", "link", "show"])
    table = []
    for line in interfaces.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            state = f"{GREEN}{parts[1]}{NC}" if parts[1] == "UP" else f"{RED}{parts[1]}{NC}"
            table.append([parts[0], state])
    print(tabulate(table, headers=["Interface", "Status"], tablefmt="grid"))
    logging.info("Listed network interfaces")

def show_ip_addresses():
    print(f"\n{BLUE}IP addresses assigned to each interface:{NC}")
    ips = execute_command(["ip", "-br", "addr", "show"])
    table = []
    for line in ips.splitlines():
        parts = line.split()
        if len(parts) >= 3:
            table.append([parts[0], f"{YELLOW}{parts[2]}{NC}"])
    print(tabulate(table, headers=["Interface", "IP Address"], tablefmt="grid"))
    logging.info("IP addresses displayed")

def show_routing_table():
    print(f"\n{BLUE}Current routing table:{NC}")
    routes = execute_command(["ip", "route", "show"])
    table = []
    for line in routes.splitlines():
        table.append([f"{GREEN}{line}{NC}"])
    print(tabulate(table, headers=["Route"], tablefmt="grid"))
    logging.info("Routing table shown")

def show_firewall_rules():
    print(f"\n{BLUE}First firewall (UFW) rules:{NC}")
    try:
        rules = execute_command(["sudo", "ufw", "status", "numbered"])
        table = []
        for line in rules.splitlines():
            if line.startswith("["):
                table.append([f"{YELLOW}{line}{NC}"])
        print(tabulate(table, headers=["UFW Rule"], tablefmt="grid"))
        logging.info("Firewall rules displayed")
    except FileNotFoundError:
        error_msg = "Error: UFW is not installed on this system."
        print(f"{RED}{error_msg}{NC}")
        logging.error(error_msg)

def list_open_connections():
    print(f"\n{BLUE}Some open network connections:{NC}")
    connections = execute_command(["ss", "-tuln"])
    table = []
    for line in connections.splitlines()[1:]:  # Omit first line (header)
        parts = line.split()
        if len(parts) >= 5:
            table.append([f"{GREEN}{parts[0]}{NC}", f"{YELLOW}{parts[4]}{NC}", f"{YELLOW}{parts[5]}{NC}"])
    print(tabulate(table, headers=["State", "Local Address", "Remote Address"], tablefmt="grid"))
    logging.info("Open network connections listed")

def print_menu():
    print(f"\n{GREEN}Network Configuration Audit Menu:{NC}")
    print("1. List network interfaces")
    print("2. Show IP addresses")
    print("3. Show routing table")
    print("4. Show firewall rules")
    print("5. List open network connections")
    print("6. Run all checks")
    print("7. Exit")

def main():
    print(f"{GREEN}Network Configuration Audit{NC}")
    logging.info("Starting network configuration audit")

    while True:
        print_menu()
        choice = input(f"{YELLOW}Enter your choice: {NC}")

        if choice == "1":
            list_interfaces()
        elif choice == "2":
            show_ip_addresses()
        elif choice == "3":
            show_routing_table()
        elif choice == "4":
            show_firewall_rules()
        elif choice == "5":
            list_open_connections()
        elif choice == "6":
            list_interfaces()
            show_ip_addresses()
            show_routing_table()
            show_firewall_rules()
            list_open_connections()
        elif choice == "7":
            print(f"{GREEN}Exiting. Thank you for using the Network Configuration Audit tool.{NC}")
            break
        else:
            print(f"{RED}Invalid choice. Please try again.{NC}")

    logging.info("Network configuration audit completed")

if __name__ == "__main__":
    main()
