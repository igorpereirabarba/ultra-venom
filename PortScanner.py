"""
Port Scanner - A beginner-friendly network utility
Scans specified IP addresses for open ports and saves results to a file.
"""

import socket
import sys
import threading
import time
from datetime import datetime
from typing import List, Dict, Tuple


class PortScanner:
    """A simple but effective port scanner for common services."""

    # Dictionary of common ports and their typical services
    COMMON_PORTS = {
        20: "FTP-DATA",
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        445: "SMB",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        5900: "VNC",
        8080: "HTTP-Alt",
        8443: "HTTPS-Alt",
    }

    def __init__(self, timeout: float = 1.0):
        """
        Initialize the port scanner.

        Args:
            timeout: Socket timeout in seconds (default: 1.0)
        """
        self.timeout = timeout
        self.open_ports = []
        self.results = []
        self.lock = threading.Lock()  # Thread safety for shared resources

    def validate_ip(self, ip_address: str) -> bool:
        """
        Validate IP address format.

        Args:
            ip_address: The IP address to validate

        Returns:
            True if valid, False otherwise
        """
        try:
            socket.inet_aton(ip_address)
            return True
        except socket.error:
            return False

    def scan_port(self, ip: str, port: int) -> bool:
        """
        Scan a single port on the specified IP address.

        Args:
            ip: Target IP address
            port: Port number to scan

        Returns:
            True if port is open, False otherwise
        """
        try:
            # Create a socket object
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)

            # Attempt to connect to the port
            result = sock.connect_ex((ip, port))
            sock.close()

            # If connect_ex returns 0, the connection was successful (port is open)
            return result == 0

        except socket.gaierror:
            print(f"Error: Could not resolve hostname {ip}")
            return False
        except socket.error:
            print(f"Error: Could not connect to {ip}")
            return False

    def scan_ports_threaded(self, ip: str, ports: List[int], num_threads: int = 10):
        """
        Scan multiple ports using threading for faster scanning.

        Args:
            ip: Target IP address
            ports: List of port numbers to scan
            num_threads: Number of threads to use (default: 10)
        """
        print(f"\n[*] Scanning {ip} for {len(ports)} ports...")
        print(f"[*] Using {num_threads} threads for faster scanning...")
        print(f"[*] Timeout: {self.timeout} second(s)\n")

        start_time = time.time()

        def worker(port_list):
            """Worker thread function to scan ports."""
            for port in port_list:
                if self.scan_port(ip, port):
                    service = self.COMMON_PORTS.get(port, "Unknown")
                    with self.lock:
                        self.open_ports.append((port, service))
                        print(f"[+] Port {port:5d} ({service:12s}) is OPEN")

        # Divide ports among threads
        ports_per_thread = len(ports) // num_threads
        threads = []

        for i in range(num_threads):
            if i == num_threads - 1:
                # Last thread gets remaining ports
                port_subset = ports[i * ports_per_thread :]
            else:
                port_subset = ports[i * ports_per_thread : (i + 1) * ports_per_thread]

            thread = threading.Thread(target=worker, args=(port_subset,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        elapsed_time = time.time() - start_time
        print(f"\n[*] Scan completed in {elapsed_time:.2f} seconds")

    def scan_address(self, ip: str) -> bool:
        """
        Scan all common ports on the specified IP address.

        Args:
            ip: Target IP address to scan

        Returns:
            True if scan was successful, False otherwise
        """
        # Validate IP address
        if not self.validate_ip(ip):
            print(f"Error: '{ip}' is not a valid IP address!")
            return False

        # Clear previous results
        self.open_ports = []

        # Get list of ports to scan
        ports = list(self.COMMON_PORTS.keys())

        # Perform the scan
        self.scan_ports_threaded(ip, ports)

        # Store results
        result_entry = {
            "ip": ip,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "open_ports": self.open_ports.copy(),
            "total_open": len(self.open_ports),
        }
        self.results.append(result_entry)

        return True

    def save_results(self, filename: str = "scan_results.txt") -> bool:
        """
        Save scan results to a text file.

        Args:
            filename: Output filename (default: "scan_results.txt")

        Returns:
            True if save was successful, False otherwise
        """
        if not self.results:
            print("Error: No scan results to save!")
            return False

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("=" * 70 + "\n")
                f.write("PORT SCANNER RESULTS\n")
                f.write("=" * 70 + "\n\n")

                for result in self.results:
                    f.write(f"Target IP: {result['ip']}\n")
                    f.write(f"Scan Time: {result['timestamp']}\n")
                    f.write(f"Open Ports Found: {result['total_open']}\n")
                    f.write("-" * 70 + "\n")

                    if result["open_ports"]:
                        f.write(f"{'Port':<10} {'Service':<20} {'Status':<15}\n")
                        f.write("-" * 70 + "\n")
                        for port, service in sorted(result["open_ports"]):
                            f.write(f"{port:<10} {service:<20} {'OPEN':<15}\n")
                    else:
                        f.write("No open ports found.\n")

                    f.write("\n" + "=" * 70 + "\n\n")

            print(f"[+] Results saved to '{filename}'")
            return True

        except IOError as e:
            print(f"Error: Could not write to file - {str(e)}")
            return False

    def display_results(self):
        """Display scan results in the console."""
        if not self.open_ports:
            print("\n[!] No open ports found.")
            return

        print("\n" + "=" * 50)
        print("OPEN PORTS SUMMARY")
        print("=" * 50)
        print(f"{'Port':<10} {'Service':<20}")
        print("-" * 50)
        for port, service in sorted(self.open_ports):
            print(f"{port:<10} {service:<20}")
        print("=" * 50)
        print(f"\nTotal open ports: {len(self.open_ports)}")


def get_user_input() -> List[str]:
    """
    Get IP addresses from user input.

    Returns:
        List of IP addresses to scan
    """
    print("\n" + "=" * 50)
    print("PORT SCANNER - IP ADDRESS INPUT")
    print("=" * 50)
    print("Enter IP addresses to scan (one per line)")
    print("Press Enter twice when done\n")

    addresses = []
    while True:
        ip = input("Enter IP address (or press Enter to finish): ").strip()

        if not ip:
            if addresses:
                break
            print("Error: Please enter at least one IP address!")
            continue

        addresses.append(ip)

    return addresses


def main():
    """Main application loop."""
    try:
        print("\n" + "=" * 50)
        print("WELCOME TO PORT SCANNER")
        print("=" * 50)

        # Get target IP addresses from user
        target_ips = get_user_input()

        # Initialize scanner
        scanner = PortScanner(timeout=1.0)

        # Scan each IP address
        for target_ip in target_ips:
            print(f"\n{'=' * 50}")
            if scanner.scan_address(target_ip):
                scanner.display_results()
            print(f"{'=' * 50}")

        # Save results to file
        if scanner.results:
            print("\n[*] Saving results...")
            save_to_file = input("Save results to file? (y/n): ").strip().lower()
            if save_to_file in ["y", "yes"]:
                filename = input("Enter filename (default: scan_results.txt): ").strip()
                if not filename:
                    filename = "scan_results.txt"
                scanner.save_results(filename)

        print("\n[+] Port scanner completed successfully!")

    except KeyboardInterrupt:
        print("\n\n[!] Scan interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
