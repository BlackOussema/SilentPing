#!/usr/bin/env python3
"""
SilentPing - Professional Network Connectivity Checker

A lightweight Python tool to test internet reachability using ICMP ping
with advanced features like batch checking, latency monitoring, and reporting.

Author: Ghariani Oussema
License: MIT
"""

import argparse
import os
import platform
import re
import socket
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict

# Configuration
VERSION = "1.0.0"
DEFAULT_COUNT = 4
DEFAULT_TIMEOUT = 5
DEFAULT_THREADS = 10

# Colors (cross-platform)
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

    @classmethod
    def disable(cls):
        cls.GREEN = cls.RED = cls.YELLOW = cls.BLUE = cls.CYAN = cls.RESET = cls.BOLD = ""


# Disable colors on Windows without ANSI support
if platform.system() == "Windows":
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except:
        Colors.disable()


@dataclass
class PingResult:
    """Represents the result of a ping operation."""
    host: str
    is_reachable: bool
    packets_sent: int = 0
    packets_received: int = 0
    packet_loss: float = 0.0
    min_latency: Optional[float] = None
    avg_latency: Optional[float] = None
    max_latency: Optional[float] = None
    error: Optional[str] = None
    timestamp: float = 0.0


def print_banner():
    """Print the tool banner."""
    banner = f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════╗
║                                                         ║
║   ███████╗██╗██╗     ███████╗███╗   ██╗████████╗       ║
║   ██╔════╝██║██║     ██╔════╝████╗  ██║╚══██╔══╝       ║
║   ███████╗██║██║     █████╗  ██╔██╗ ██║   ██║          ║
║   ╚════██║██║██║     ██╔══╝  ██║╚██╗██║   ██║          ║
║   ███████║██║███████╗███████╗██║ ╚████║   ██║          ║
║   ╚══════╝╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝          ║
║                    PING v{VERSION}                        ║
║              by Ghariani Oussema 🇹🇳                    ║
╚═══════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)


def resolve_hostname(host: str) -> Optional[str]:
    """Resolve hostname to IP address."""
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        return None


def ping_host(
    host: str,
    count: int = DEFAULT_COUNT,
    timeout: int = DEFAULT_TIMEOUT
) -> PingResult:
    """
    Ping a host and return detailed results.
    
    Args:
        host: Hostname or IP address to ping
        count: Number of ping packets to send
        timeout: Timeout in seconds
    
    Returns:
        PingResult object with ping statistics
    """
    result = PingResult(host=host, is_reachable=False, timestamp=time.time())
    
    # Determine ping command based on OS
    system = platform.system().lower()
    
    if system == "windows":
        cmd = ["ping", "-n", str(count), "-w", str(timeout * 1000), host]
    else:  # Linux, macOS
        cmd = ["ping", "-c", str(count), "-W", str(timeout), host]
    
    try:
        output = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout * count + 5
        )
        
        stdout = output.stdout
        
        # Parse results based on OS
        if system == "windows":
            result = _parse_windows_ping(host, stdout, result)
        else:
            result = _parse_unix_ping(host, stdout, result)
        
        result.is_reachable = result.packets_received > 0
        
    except subprocess.TimeoutExpired:
        result.error = "Ping timed out"
    except FileNotFoundError:
        result.error = "Ping command not found"
    except Exception as e:
        result.error = str(e)
    
    return result


def _parse_unix_ping(host: str, output: str, result: PingResult) -> PingResult:
    """Parse Unix/Linux/macOS ping output."""
    # Parse packet statistics
    # Example: "4 packets transmitted, 4 received, 0% packet loss"
    stats_match = re.search(
        r"(\d+)\s+packets?\s+transmitted,\s+(\d+)\s+(?:packets?\s+)?received",
        output
    )
    if stats_match:
        result.packets_sent = int(stats_match.group(1))
        result.packets_received = int(stats_match.group(2))
        if result.packets_sent > 0:
            result.packet_loss = ((result.packets_sent - result.packets_received) / result.packets_sent) * 100
    
    # Parse latency statistics
    # Example: "rtt min/avg/max/mdev = 10.123/15.456/20.789/3.456 ms"
    latency_match = re.search(
        r"(?:rtt|round-trip)\s+min/avg/max(?:/\w+)?\s*=\s*([\d.]+)/([\d.]+)/([\d.]+)",
        output
    )
    if latency_match:
        result.min_latency = float(latency_match.group(1))
        result.avg_latency = float(latency_match.group(2))
        result.max_latency = float(latency_match.group(3))
    
    return result


def _parse_windows_ping(host: str, output: str, result: PingResult) -> PingResult:
    """Parse Windows ping output."""
    # Parse packet statistics
    # Example: "Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)"
    stats_match = re.search(
        r"Sent\s*=\s*(\d+),\s*Received\s*=\s*(\d+)",
        output
    )
    if stats_match:
        result.packets_sent = int(stats_match.group(1))
        result.packets_received = int(stats_match.group(2))
        if result.packets_sent > 0:
            result.packet_loss = ((result.packets_sent - result.packets_received) / result.packets_sent) * 100
    
    # Parse latency statistics
    # Example: "Minimum = 10ms, Maximum = 20ms, Average = 15ms"
    latency_match = re.search(
        r"Minimum\s*=\s*(\d+)ms,\s*Maximum\s*=\s*(\d+)ms,\s*Average\s*=\s*(\d+)ms",
        output
    )
    if latency_match:
        result.min_latency = float(latency_match.group(1))
        result.max_latency = float(latency_match.group(2))
        result.avg_latency = float(latency_match.group(3))
    
    return result


def print_result(result: PingResult, verbose: bool = False):
    """Print ping result with colors."""
    if result.is_reachable:
        status = f"{Colors.GREEN}✓ REACHABLE{Colors.RESET}"
        latency_str = ""
        if result.avg_latency is not None:
            latency_str = f" (avg: {result.avg_latency:.1f}ms)"
        print(f"{status} {result.host}{latency_str}")
        
        if verbose and result.min_latency is not None:
            print(f"  └─ Packets: {result.packets_received}/{result.packets_sent} "
                  f"| Loss: {result.packet_loss:.1f}% "
                  f"| Latency: {result.min_latency:.1f}/{result.avg_latency:.1f}/{result.max_latency:.1f} ms")
    else:
        status = f"{Colors.RED}✗ UNREACHABLE{Colors.RESET}"
        error_str = f" ({result.error})" if result.error else ""
        print(f"{status} {result.host}{error_str}")


def ping_multiple(
    hosts: List[str],
    count: int = DEFAULT_COUNT,
    timeout: int = DEFAULT_TIMEOUT,
    threads: int = DEFAULT_THREADS,
    verbose: bool = False
) -> List[PingResult]:
    """
    Ping multiple hosts concurrently.
    
    Args:
        hosts: List of hostnames or IP addresses
        count: Number of ping packets per host
        timeout: Timeout in seconds
        threads: Number of concurrent threads
        verbose: Show detailed output
    
    Returns:
        List of PingResult objects
    """
    results = []
    
    print(f"\n{Colors.CYAN}[*] Pinging {len(hosts)} host(s)...{Colors.RESET}\n")
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(ping_host, host, count, timeout): host
            for host in hosts
        }
        
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print_result(result, verbose)
    
    return results


def print_summary(results: List[PingResult]):
    """Print summary of ping results."""
    total = len(results)
    reachable = sum(1 for r in results if r.is_reachable)
    unreachable = total - reachable
    
    avg_latencies = [r.avg_latency for r in results if r.avg_latency is not None]
    overall_avg = sum(avg_latencies) / len(avg_latencies) if avg_latencies else 0
    
    print(f"\n{Colors.CYAN}{'='*50}{Colors.RESET}")
    print(f"{Colors.BOLD}Summary:{Colors.RESET}")
    print(f"  Total hosts: {total}")
    print(f"  {Colors.GREEN}Reachable: {reachable}{Colors.RESET}")
    print(f"  {Colors.RED}Unreachable: {unreachable}{Colors.RESET}")
    if avg_latencies:
        print(f"  Average latency: {overall_avg:.1f}ms")
    print(f"{Colors.CYAN}{'='*50}{Colors.RESET}")


def save_results(results: List[PingResult], output_path: str):
    """Save results to file."""
    with open(output_path, "w") as f:
        f.write("Host,Reachable,Packets Sent,Packets Received,Loss %,Min Latency,Avg Latency,Max Latency\n")
        for r in results:
            f.write(f"{r.host},{r.is_reachable},{r.packets_sent},{r.packets_received},"
                    f"{r.packet_loss:.1f},{r.min_latency or ''},{r.avg_latency or ''},{r.max_latency or ''}\n")
    
    print(f"\n{Colors.GREEN}[+] Results saved to {output_path}{Colors.RESET}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="SilentPing - Professional Network Connectivity Checker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s google.com
  %(prog)s 8.8.8.8 1.1.1.1 cloudflare.com
  %(prog)s -f hosts.txt -c 10 -v
  %(prog)s google.com -o results.csv
        """
    )
    
    parser.add_argument(
        "hosts",
        nargs="*",
        help="Host(s) to ping"
    )
    parser.add_argument(
        "-f", "--file",
        help="File containing hosts (one per line)"
    )
    parser.add_argument(
        "-c", "--count",
        type=int,
        default=DEFAULT_COUNT,
        help=f"Number of ping packets (default: {DEFAULT_COUNT})"
    )
    parser.add_argument(
        "-t", "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Timeout in seconds (default: {DEFAULT_TIMEOUT})"
    )
    parser.add_argument(
        "-T", "--threads",
        type=int,
        default=DEFAULT_THREADS,
        help=f"Number of threads for batch pinging (default: {DEFAULT_THREADS})"
    )
    parser.add_argument(
        "-o", "--output",
        help="Save results to CSV file"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed output"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Quiet mode (no banner)"
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"SilentPing v{VERSION}"
    )
    
    args = parser.parse_args()
    
    # Disable colors if requested
    if args.no_color:
        Colors.disable()
    
    # Print banner
    if not args.quiet:
        print_banner()
    
    # Collect hosts
    hosts = list(args.hosts) if args.hosts else []
    
    if args.file:
        if not os.path.isfile(args.file):
            print(f"{Colors.RED}[!] File not found: {args.file}{Colors.RESET}")
            sys.exit(1)
        
        with open(args.file, "r") as f:
            file_hosts = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            hosts.extend(file_hosts)
    
    if not hosts:
        parser.print_help()
        sys.exit(1)
    
    # Remove duplicates while preserving order
    hosts = list(dict.fromkeys(hosts))
    
    # Ping hosts
    if len(hosts) == 1:
        result = ping_host(hosts[0], args.count, args.timeout)
        print()
        print_result(result, args.verbose)
        results = [result]
    else:
        results = ping_multiple(
            hosts,
            count=args.count,
            timeout=args.timeout,
            threads=args.threads,
            verbose=args.verbose
        )
        print_summary(results)
    
    # Save results
    if args.output:
        save_results(results, args.output)
    
    # Exit code based on results
    sys.exit(0 if all(r.is_reachable for r in results) else 1)


if __name__ == "__main__":
    main()
