<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Platform-Cross--Platform-lightgrey.svg" alt="Platform">
</p>

<h1 align="center">🔇 SilentPing</h1>

<p align="center">
  <strong>Professional Network Connectivity Checker</strong>
</p>

<p align="center">
  A lightweight Python tool to test internet reachability using ICMP ping<br>
  with batch checking, latency monitoring, and detailed reporting.
</p>

---

## ✨ Features

- **Single & Batch Pinging** - Check one or multiple hosts
- **Concurrent Scanning** - Multithreaded for fast batch operations
- **Detailed Statistics** - Packet loss, min/avg/max latency
- **Cross-Platform** - Works on Windows, Linux, and macOS
- **File Input** - Load hosts from a file
- **CSV Export** - Save results for analysis
- **Colored Output** - Easy-to-read status indicators

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/BlackOussema/SilentPing.git
cd SilentPing

# No dependencies required - uses standard library only!
```

### Basic Usage

```bash
# Ping a single host
python silentping.py google.com

# Ping multiple hosts
python silentping.py google.com 8.8.8.8 cloudflare.com

# Ping hosts from file
python silentping.py -f hosts.txt

# Verbose output with more details
python silentping.py google.com -v
```

---

## 📖 Usage

```
usage: silentping.py [-h] [-f FILE] [-c COUNT] [-t TIMEOUT] [-T THREADS]
                     [-o OUTPUT] [-v] [-q] [--no-color] [--version]
                     [hosts ...]

Options:
  hosts                 Host(s) to ping
  -f, --file FILE       File containing hosts (one per line)
  -c, --count N         Number of ping packets (default: 4)
  -t, --timeout SEC     Timeout in seconds (default: 5)
  -T, --threads N       Threads for batch pinging (default: 10)
  -o, --output FILE     Save results to CSV file
  -v, --verbose         Show detailed output
  -q, --quiet           No banner
  --no-color            Disable colored output
  --version             Show version
```

---

## 💡 Examples

### Single Host
```bash
python silentping.py google.com
```
Output:
```
✓ REACHABLE google.com (avg: 15.2ms)
```

### Multiple Hosts
```bash
python silentping.py google.com 8.8.8.8 1.1.1.1 cloudflare.com
```

### Verbose Mode
```bash
python silentping.py google.com -v -c 10
```
Output:
```
✓ REACHABLE google.com (avg: 15.2ms)
  └─ Packets: 10/10 | Loss: 0.0% | Latency: 12.1/15.2/18.5 ms
```

### From File
```bash
# hosts.txt:
# google.com
# 8.8.8.8
# cloudflare.com

python silentping.py -f hosts.txt
```

### Export Results
```bash
python silentping.py -f hosts.txt -o results.csv
```

---

## 📊 Output Formats

### Console Output
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
```csv
Host,Reachable,Packets Sent,Packets Received,Loss %,Min Latency,Avg Latency,Max Latency
google.com,True,4,4,0.0,12.1,15.2,18.5
8.8.8.8,True,4,4,0.0,8.2,10.5,12.8
badhost.invalid,False,4,0,100.0,,,
```

---

## 🔧 Configuration

### Hosts File Format

Create a text file with one host per line:

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

Lines starting with `#` are treated as comments.

---

## 📋 Requirements

**No external dependencies!** Uses Python standard library only.

- Python 3.8+
- `ping` command (available on all major operating systems)

---

## 🖥️ Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| Linux | ✅ Full | Uses `ping -c` |
| macOS | ✅ Full | Uses `ping -c` |
| Windows | ✅ Full | Uses `ping -n` |

---

## 🔒 Use Cases

### Network Monitoring
```bash
# Check critical infrastructure every minute
watch -n 60 python silentping.py -f critical-hosts.txt -q
```

### Connectivity Testing
```bash
# Test internet connectivity
python silentping.py google.com cloudflare.com -c 10
```

### Server Health Checks
```bash
# Check server availability
python silentping.py server1.local server2.local db.local -o health.csv
```

### Troubleshooting
```bash
# Detailed latency analysis
python silentping.py problematic-host.com -c 20 -v
```

---

## 🤝 Contributing

Contributions are welcome! Ideas:

- Add TCP ping support
- Implement continuous monitoring mode
- Add JSON output format
- Create web dashboard
- Add email/webhook alerts

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

**Ghariani Oussema**
- GitHub: [@BlackOussema](https://github.com/BlackOussema)
- Role: Cyber Security Researcher & Full-Stack Developer
- Location: Tunisia 🇹🇳

---

<p align="center">
  Made with ❤️ in Tunisia 🇹🇳
</p>
