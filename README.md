# 🔇 SilentPing: Professional Network Connectivity Checker

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Cross--Platform-lightgrey.svg)

## Overview

SilentPing is a lightweight and efficient Python tool designed to test network reachability and monitor latency using ICMP (Internet Control Message Protocol) ping. It supports checking single or multiple hosts, offers concurrent batch processing, and provides detailed statistics including packet loss and average latency. This cross-platform utility is ideal for network administrators, developers, and anyone needing a reliable way to assess network connectivity.

## Features

*   **Single & Batch Pinging**: Test connectivity to a single host or multiple hosts simultaneously.
*   **Concurrent Scanning**: Utilizes multithreading for fast and efficient batch operations, significantly reducing the time required to check numerous hosts.
*   **Detailed Statistics**: Provides comprehensive ping statistics, including packet loss percentage, minimum, average, and maximum latency.
*   **Cross-Platform Compatibility**: Works seamlessly on Windows, Linux, and macOS, leveraging the native `ping` command.
*   **File Input**: Load a list of target hosts from a text file (one host per line) for automated checks.
*   **CSV Export**: Save detailed results to a CSV file for further analysis, reporting, or integration with other tools.
*   **Colored Output**: Easy-to-read console output with color-coded status indicators for quick identification of reachable and unreachable hosts.

## Quick Start

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/BlackOussema/SilentPing.git
    cd SilentPing
    ```

2.  **No external dependencies required!** SilentPing uses only Python's standard library and the system's native `ping` command.

### Basic Usage

*   **Ping a single host**:
    ```bash
    python silentping.py google.com
    ```

*   **Ping multiple hosts**:
    ```bash
    python silentping.py google.com 8.8.8.8 cloudflare.com
    ```

*   **Ping hosts from a file**:
    ```bash
    python silentping.py -f hosts.txt
    ```

*   **Verbose output with more details**:
    ```bash
    python silentping.py google.com -v
    ```

## Usage

```
usage: silentping.py [-h] [-f FILE] [-c COUNT] [-t TIMEOUT] [-T THREADS]
                     [-o OUTPUT] [-v] [-q] [--no-color] [--version]
                     [hosts ...]

positional arguments:
  hosts                 One or more hostnames or IP addresses to ping.

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Path to a file containing hosts (one per line).
  -c COUNT, --count N   Number of ICMP packets to send per host (default: 4).
  -t TIMEOUT, --timeout SEC
                        Timeout in seconds for each ping attempt (default: 5).
  -T THREADS, --threads N
                        Number of concurrent threads for batch pinging (default: 10).
  -o OUTPUT, --output FILE
                        Path to a CSV file to save results.
  -v, --verbose         Show detailed output for each host.
  -q, --quiet           Suppress the initial banner message.
  --no-color            Disable colored console output.
  --version             Show the tool's version and exit.
```

## Examples

### Single Host Ping
```bash
python silentping.py example.com
```
**Output Example**:
```
✓ REACHABLE example.com (avg: 25.3ms)
```

### Multiple Hosts Ping
```bash
python silentping.py google.com 8.8.8.8 1.1.1.1 cloudflare.com
```

### Verbose Mode
```bash
python silentping.py google.com -v -c 10
```
**Output Example**:
```
✓ REACHABLE google.com (avg: 15.2ms)
  └─ Packets: 10/10 | Loss: 0.0% | Latency: 12.1/15.2/18.5 ms
```

### Pinging from a File

`hosts.txt` content:
```
# My important servers
server1.local
192.168.1.1
google.com
```

Run command:
```bash
python silentping.py -f hosts.txt
```

### Exporting Results to CSV
```bash
python silentping.py -f hosts.txt -o results.csv
```

## Output Formats

### Console Output

SilentPing provides a clear and concise console output, with a summary at the end:

```
✓ REACHABLE google.com (avg: 15.2ms)
✓ REACHABLE 8.8.8.8 (avg: 10.5ms)
✗ UNREACHABLE badhost.invalid (Name or service not known)

==================================================
Summary:
  Total hosts: 3
  Reachable: 2
  Unreachable: 1
  Average latency: 12.8ms
==================================================
```

### CSV Output

When using the `-o` or `--output` option, results are saved in a CSV format, suitable for spreadsheet applications:

```csv
Host,Reachable,Packets Sent,Packets Received,Loss %,Min Latency,Avg Latency,Max Latency
google.com,True,4,4,0.0,12.1,15.2,18.5
8.8.8.8,True,4,4,0.0,8.2,10.5,12.8
badhost.invalid,False,4,0,100.0,,,
```

## Configuration

### Hosts File Format

Hosts files should contain one hostname or IP address per line. Lines starting with `#` are treated as comments and ignored.

```
# Network infrastructure
8.8.8.8
8.8.4.4
1.1.1.1

# Web services
google.com
cloudflare.com
github.com

# Internal servers
192.168.1.1
server.local
```

## Requirements

*   **Python 3.8+**: The tool is written in Python and requires version 3.8 or newer.
*   **`ping` command**: Relies on the native `ping` command available on all major operating systems (Linux, macOS, Windows).

## Platform Support

| Platform    | Status    | Notes                                       |
|-------------|-----------|---------------------------------------------|
| Linux       | ✅ Full   | Uses `ping -c` for packet count.            |
| macOS       | ✅ Full   | Uses `ping -c` for packet count.            |
| Windows     | ✅ Full   | Uses `ping -n` for packet count.            |

## Use Cases

### Network Monitoring
```bash
# Check critical infrastructure every minute (using watch command)
watch -n 60 python silentping.py -f critical-hosts.txt -q
```

### Connectivity Testing
```bash
# Test general internet connectivity
python silentping.py google.com cloudflare.com -c 10
```

### Server Health Checks
```bash
# Monitor availability of internal servers
python silentping.py server1.local server2.local db.local -o health.csv
```

### Troubleshooting Network Issues
```bash
# Detailed latency analysis for a problematic host
python silentping.py problematic-host.com -c 20 -v
```

## Contributing

Contributions are welcome! If you have ideas for new features, improvements, or bug fixes, please consider:

*   Adding TCP ping support.
*   Implementing a continuous monitoring mode.
*   Adding a JSON output format for programmatic use.
*   Creating a web dashboard for real-time visualization.
*   Integrating email or webhook alerts for connectivity issues.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for full details.

## Author

**Ghariani Oussema**
*   GitHub: [@BlackOussema](https://github.com/BlackOussema)
*   Role: Cybersecurity Researcher & Full-Stack Developer
*   Location: Tunisia 🇹🇳

---

<p align="center">
  Made with ❤️ in Tunisia 🇹🇳
</p>
