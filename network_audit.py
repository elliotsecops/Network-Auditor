import subprocess
import logging
import json
from tabulate import tabulate
import getpass
from logging.handlers import RotatingFileHandler
import argparse

# Configure logging
handler = RotatingFileHandler('audit_network.log', maxBytes=1000000, backupCount=5)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', handlers=[handler])

# ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
NC = '\033[0m'  # No Color

def execute_command(command, **kwargs):
    """Execute a command and return its output or log an error."""
    try:
        result = subprocess.run(command, shell=False, capture_output=True, text=True, check=True, **kwargs)
        return result.stdout
    except subprocess.CalledProcessError as e:
        error_msg = f"Error executing {' '.join(command)}: {e.stderr}"
        logging.error(error_msg)
        return None

def list_interfaces():
    """List network interfaces and their status."""
    print(f"\n{BLUE}Network interfaces and their status:{NC}")
    interfaces = execute_command(["ip", "-br", "link", "show"])
    if interfaces is None:
        return False
    table = []
    for line in interfaces.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            state = f"{GREEN}{parts[1]}{NC}" if parts[1] == "UP" else f"{RED}{parts[1]}{NC}"
            table.append([parts[0], state])
    print(tabulate(table, headers=["Interface", "Status"], tablefmt="grid"))
    logging.info("Listed network interfaces")
    return True

def show_ip_addresses():
    """Show IP addresses assigned to each interface."""
    print(f"\n{BLUE}IP addresses assigned to each interface:{NC}")
    ips = execute_command(["ip", "-br", "addr", "show"])
    if ips is None:
        return False
    table = []
    for line in ips.splitlines():
        parts = line.split()
        if len(parts) >= 3:
            table.append([parts[0], f"{YELLOW}{parts[2]}{NC}"])
    print(tabulate(table, headers=["Interface", "IP Address"], tablefmt="grid"))
    logging.info("IP addresses displayed")
    return True

def show_routing_table():
    """Show the current routing table."""
    print(f"\n{BLUE}Current routing table:{NC}")
    routes = execute_command(["ip", "route", "show"])
    if routes is None:
        return False
    table = []
    for line in routes.splitlines():
        table.append([f"{GREEN}{line}{NC}"])
    print(tabulate(table, headers=["Route"], tablefmt="grid"))
    logging.info("Routing table shown")
    return True

def show_firewall_rules():
    """Show UFW firewall rules."""
    print(f"\n{BLUE}UFW firewall rules:{NC}")
    try:
        password = getpass.getpass("Enter your sudo password: ")
        rules = execute_command(["sudo", "-S", "ufw", "status", "numbered"], input=password.encode())
        if rules is None:
            return False
        table = []
        for line in rules.splitlines():
            if line.startswith("["):
                table.append([f"{YELLOW}{line}{NC}"])
        print(tabulate(table, headers=["UFW Rule"], tablefmt="grid"))
        logging.info("Firewall rules displayed")
        return True
    except FileNotFoundError:
        error_msg = "Error: UFW is not installed on this system."
        print(f"{RED}{error_msg}{NC}")
        logging.error(error_msg)
        return False

def list_open_connections():
    """List open network connections."""
    print(f"\n{BLUE}Open network connections:{NC}")
    connections = execute_command(["ss", "-tuln"])
    if connections is None:
        return False
    table = []
    for line in connections.splitlines()[1:]:  # Omit first line (header)
        parts = line.split()
        if len(parts) >= 5:
            table.append([f"{GREEN}{parts[0]}{NC}", f"{YELLOW}{parts[4]}{NC}", f"{YELLOW}{parts[5]}{NC}"])
    print(tabulate(table, headers=["State", "Local Address", "Remote Address"], tablefmt="grid"))
    logging.info("Open network connections listed")
    return True

def list_docker_nets():
    """List Docker networks and their associated IP addresses."""
    print(f"\n{BLUE}Docker Networks:{NC}")
    found = subprocess.run(['which', 'docker'], capture_output=True, text=True)
    if found.returncode != 0:
        error_msg = "Docker not found."
        print(f"{RED}{error_msg}{NC}")
        logging.warning(error_msg)
        return False

    nets = execute_command(['docker', 'network', 'ls'])
    if nets is None:
        return False

    try:
        net_names = [line.split()[1] for line in nets.splitlines()[1:] if len(line.split()) >= 4]
        if not net_names:
            print("No Docker networks found.")
            return True

        inspect_output = execute_command(['docker', 'network', 'inspect'] + net_names)
        if inspect_output is None:
            return False
        data = json.loads(inspect_output)
        table = []
        for network in data:
            net_name = network['Name']
            table.append([f"{GREEN}{net_name}{NC}", "", ""])
            containers = network.get('Containers', {})
            for container in containers.values():
                table.append([f"", f"{YELLOW}{container['Name']}{NC}", f"{YELLOW}{container['IPv4Address']}{NC}"])
        print(tabulate(table, headers=["Network Name", "Host Name", "Host IP"], tablefmt="grid"))
        logging.info("Docker network connections listed")
        return True
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        error_msg = f"Error inspecting Docker networks: {e}"
        print(f"{RED}{error_msg}{NC}")
        logging.error(error_msg)
        return False

def print_menu():
    """Print the interactive menu."""
    print(f"\n{GREEN}Network Configuration Audit Menu:{NC}")
    print("1. List network interfaces")
    print("2. Show IP addresses")
    print("3. Show routing table")
    print("4. Show firewall rules")
    print("5. List open network connections")
    print("6. List Docker networks")
    print("7. Run all checks")
    print("8. Exit")

def run_all_checks():
    """Run all network configuration checks."""
    print(f"{BLUE}Running all checks...{NC}")
    if not list_interfaces():
        print(f"{RED}Error listing interfaces.{NC}")
    print(f"{GREEN}Interface check complete.{NC}")

    print(f"{BLUE}Checking IP addresses...{NC}")
    if not show_ip_addresses():
        print(f"{RED}Error showing IP addresses.{NC}")
    print(f"{GREEN}IP address check complete.{NC}")

    print(f"{BLUE}Checking routing table...{NC}")
    if not show_routing_table():
        print(f"{RED}Error showing routing table.{NC}")
    print(f"{GREEN}Routing table check complete.{NC}")

    print(f"{BLUE}Checking firewall rules...{NC}")
    if not show_firewall_rules():
        print(f"{RED}Error showing firewall rules.{NC}")
    print(f"{GREEN}Firewall rules check complete.{NC}")

    print(f"{BLUE}Checking open network connections...{NC}")
    if not list_open_connections():
        print(f"{RED}Error listing open connections.{NC}")
    print(f"{GREEN}Open connections check complete.{NC}")

    print(f"{BLUE}Checking Docker networks...{NC}")
    if not list_docker_nets():
        print(f"{RED}Error listing Docker networks.{NC}")
    print(f"{GREEN}Docker networks check complete.{NC}")

def exit_program():
    """Exit the program gracefully."""
    print(f"{GREEN}Exiting. Thank you for using the Network Configuration Audit tool.{NC}")
    logging.info("Network configuration audit completed")

def main():
    """Main function to run the network configuration audit."""
    parser = argparse.ArgumentParser(prog='network-auditor', description="Network Configuration Audit")
    parser.add_argument("--all", action="store_true", help="Run all checks")
    args = parser.parse_args()

    if args.all:
        run_all_checks()
        return 0

    print(f"{GREEN}Network Configuration Audit{NC}")
    logging.info("Starting network configuration audit")

    while True:
        print_menu()
        try:
            choice = int(input(f"{YELLOW}Enter your choice: {NC}"))
            if 1 <= choice <= 8:
                break
            else:
                print(f"{RED}Invalid choice. Please enter a number between 1 and 8.{NC}")
        except ValueError:
            print(f"{RED}Invalid input. Please enter a number.{NC}")

    actions = {
        1: list_interfaces,
        2: show_ip_addresses,
        3: show_routing_table,
        4: show_firewall_rules,
        5: list_open_connections,
        6: list_docker_nets,
        7: run_all_checks,
        8: exit_program
    }

    action = actions.get(choice)
    if action:
        action()
    else:
        print(f"{RED}Invalid choice (internal error).{NC}")

    return 0

if __name__ == "__main__":
    main()
