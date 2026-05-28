# Port Scanner - Network Utility

A beginner-friendly Python port scanner that detects open ports on specified IP addresses and saves results to a text file.

## Features

- ✅ **Scan Common Ports**: Scans 17 commonly used service ports (SSH, HTTP, HTTPS, MySQL, etc.)
- ✅ **Multi-threaded Scanning**: Fast scanning using threading (10 threads by default)
- ✅ **Input Validation**: Validates IP address format before scanning
- ✅ **Save Results**: Export scan results to a formatted text file
- ✅ **Error Handling**: Comprehensive error handling for network issues
- ✅ **Clean Code**: Well-documented, modular code structure
- ✅ **Service Identification**: Identifies common services running on open ports

## Installation

### Requirements
- Python 3.6 or higher
- No external dependencies (uses only standard library)

### Setup

1. Clone or download the project:
```bash
# Option 1: If you have git
git clone <repository-url>

# Option 2: Direct download
# Download PortScanner.py and README.md
```

2. Navigate to the project directory:
```bash
cd port-scanner
```

3. Run the scanner:
```bash
python PortScanner.py
```

## Usage

### Interactive Mode

Simply run the script and follow the prompts:

```bash
python PortScanner.py
```

**Example Session:**
```
==================================================
WELCOME TO PORT SCANNER
==================================================

==================================================
PORT SCANNER - IP ADDRESS INPUT
==================================================
Enter IP addresses to scan (one per line)
Press Enter twice when done

Enter IP address (or press Enter to finish): 192.168.1.1
Enter IP address (or press Enter to finish): 8.8.8.8
Enter IP address (or press Enter to finish):

==================================================
[*] Scanning 192.168.1.1 for 17 ports...
[*] Using 10 threads for faster scanning...
[*] Timeout: 1.0 second(s)

[+] Port    22   (SSH          ) is OPEN
[+] Port    80   (HTTP         ) is OPEN
[+] Port   443   (HTTPS        ) is OPEN

[*] Scan completed in 2.45 seconds

==================================================
OPEN PORTS SUMMARY
==================================================
Port       Service
--------------------------------------------------
22         SSH
80         HTTP
443        HTTPS
==================================================

Total open ports: 3
```

### Scanning Specific IPs

The scanner supports scanning:
- **Single IP**: `192.168.1.1`
- **Multiple IPs**: Enter multiple addresses one per line
- **Localhost**: `127.0.0.1`
- **Public IPs**: `8.8.8.8` (Google DNS)

### Saving Results

After scanning, you'll be prompted to save results:
```
Save results to file? (y/n): y
Enter filename (default: scan_results.txt): my_scan.txt
[+] Results saved to 'my_scan.txt'
```

## Scanned Ports

The scanner checks for these common service ports:

| Port | Service | Use Case |
|------|---------|----------|
| 20 | FTP-DATA | File Transfer |
| 21 | FTP | File Transfer |
| 22 | SSH | Secure Shell |
| 23 | Telnet | Remote Login |
| 25 | SMTP | Email Sending |
| 53 | DNS | Domain Name System |
| 80 | HTTP | Web Server |
| 110 | POP3 | Email Retrieval |
| 143 | IMAP | Email Retrieval |
| 443 | HTTPS | Secure Web |
| 445 | SMB | File Sharing |
| 3306 | MySQL | Database |
| 3389 | RDP | Remote Desktop |
| 5432 | PostgreSQL | Database |
| 5900 | VNC | Remote Display |
| 8080 | HTTP-Alt | Alt Web Server |
| 8443 | HTTPS-Alt | Alt Secure Web |

## Code Structure

### Main Classes

**PortScanner**
- `__init__(timeout)`: Initialize scanner with socket timeout
- `validate_ip(ip_address)`: Validate IP address format
- `scan_port(ip, port)`: Scan single port
- `scan_ports_threaded(ip, ports, num_threads)`: Multi-threaded port scanning
- `scan_address(ip)`: Scan all common ports on an IP
- `save_results(filename)`: Save results to file
- `display_results()`: Display results in console

### Main Functions

- `get_user_input()`: Get target IPs from user
- `main()`: Application entry point

## Examples

### Example 1: Scan Local Network Gateway

```bash
python PortScanner.py
# Enter: 192.168.1.1
```

### Example 2: Scan Multiple Servers

```bash
python PortScanner.py
# Enter: 192.168.1.10
# Enter: 192.168.1.20
# Enter: 192.168.1.30
# Press Enter to finish
```

### Example 3: Scan and Save Results

```bash
python PortScanner.py
# Enter target IP
# When prompted, save results to "network_audit.txt"
```

## Output Files

When you save results, a text file is created with this format:

```
======================================================================
PORT SCANNER RESULTS
======================================================================

Target IP: 192.168.1.1
Scan Time: 2026-05-28 14:30:45
Open Ports Found: 3
----------------------------------------------------------------------
Port       Service              Status
----------------------------------------------------------------------
22         SSH                  OPEN
80         HTTP                 OPEN
443        HTTPS                OPEN

======================================================================
```

## Important Notes

### Legal and Ethical Considerations

⚠️ **WARNING**: Only scan IP addresses you own or have explicit permission to scan.

- Unauthorized port scanning may be illegal in your jurisdiction
- Always get written permission before scanning network infrastructure
- Use this tool responsibly and ethically
- Test on your own systems first

### Technical Notes

- **Timeout**: Default is 1 second per port. Adjust in code if needed
- **Threading**: Default 10 threads for balance between speed and stability
- **Firewall**: Firewalls may block scans or return misleading results
- **False Positives**: Firewalls may respond as if ports are open when they're blocked

## Troubleshooting

### No Open Ports Found
- Check if the IP address is correct
- Verify network connectivity to the target
- Firewall may be blocking all ports
- Increase timeout in code if network is slow

### "Invalid IP Address" Error
- Ensure IP is in valid format (e.g., `192.168.1.1`)
- Don't include protocol prefix (no `http://`)
- Check for typos

### Script Runs Slowly
- Target host may be down or unreachable
- Network latency is high
- Firewall is slow to respond
- Try reducing number of threads in code

### Permission Denied Error
- File already open in another program
- Check write permissions in directory
- Try specifying full path for filename

## Customization

### Change Timeout
Edit `PortScanner.py` line in `main()`:
```python
scanner = PortScanner(timeout=2.0)  # Change to 2 seconds
```

### Add More Ports
Edit `COMMON_PORTS` dictionary in the `PortScanner` class:
```python
COMMON_PORTS = {
    # ... existing ports ...
    9000: "Custom Service",
}
```

### Change Number of Threads
Edit `scan_ports_threaded()` call:
```python
scanner.scan_ports_threaded(ip, ports, num_threads=20)
```

## Learning Points

This project demonstrates several programming concepts:

1. **Object-Oriented Programming**: Class design and encapsulation
2. **Network Programming**: Socket API usage
3. **Threading**: Concurrent execution with thread synchronization
4. **Input Validation**: Data validation and error handling
5. **File I/O**: Reading/writing files
6. **Type Hints**: Python type annotations
7. **String Formatting**: F-strings and format()
8. **Exception Handling**: Try-except blocks

## Performance

- **Typical Scan Time**: 2-5 seconds for 17 ports (with 10 threads)
- **Speed-up**: Threading provides 8-10x speedup vs sequential scanning
- **Memory Usage**: Minimal (threading overhead is low)

## Requirements

- Python 3.6+
- Standard library only (socket, threading, sys, etc.)
- Works on Windows, macOS, and Linux

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review code comments
3. Verify network connectivity
4. Check firewall settings

## Future Enhancements

Possible additions for advanced users:

- [ ] UDP port scanning
- [ ] Custom port ranges
- [ ] Ping/ICMP detection
- [ ] Service version detection
- [ ] CSV export
- [ ] GUI interface
- [ ] Scheduled scanning
- [ ] Database storage

---

**Created**: 2026-05-28  
**Version**: 1.0  
**Language**: Python 3.6+
