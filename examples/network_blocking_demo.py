#!/usr/bin/env worm
"""
Example: Network Blocking Demonstration

This script demonstrates how Worm Python blocks network operations
while allowing all other Python functionality to work normally.
"""

import os
import sys


def test_allowed_operations():
    """Demonstrate operations that are allowed."""
    print("=== Testing Allowed Operations ===\n")

    # Basic I/O
    print("✓ Print to stdout works")

    # Math
    import math
    result = math.sqrt(42)
    print(f"✓ Math operations work: sqrt(42) = {result:.2f}")

    # Data structures
    data = {'name': 'Worm Python', 'status': 'secure'}
    print(f"✓ Data structures work: {data}")

    # File I/O
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("test data")
        temp_file = f.name
    with open(temp_file, 'r') as f:
        content = f.read()
    os.unlink(temp_file)
    print(f"✓ File I/O works: wrote and read '{content}'")

    # JSON
    import json
    json_str = json.dumps({'test': 'ok'})
    print(f"✓ JSON works: {json_str}")

    # Safe subprocess
    import subprocess
    result = subprocess.run(['echo', 'subprocess works'],
                          capture_output=True, text=True)
    print(f"✓ Safe subprocess works: {result.stdout.strip()}")

    print()


def test_blocked_operations():
    """Demonstrate operations that are blocked."""
    print("=== Testing Blocked Network Operations ===\n")

    # Test 1: socket module
    print("Test 1: Importing socket module...")
    try:
        import socket
        print("  ✗ FAIL: socket was not blocked!")
    except ImportError as e:
        print(f"  ✓ PASS: socket blocked - {str(e)[:60]}...")

    # Test 2: urllib
    print("\nTest 2: Importing urllib.request...")
    try:
        import urllib.request
        print("  ✗ FAIL: urllib.request was not blocked!")
    except ImportError as e:
        print(f"  ✓ PASS: urllib blocked - {str(e)[:60]}...")

    # Test 3: http module
    print("\nTest 3: Importing http.client...")
    try:
        import http.client
        print("  ✗ FAIL: http.client was not blocked!")
    except ImportError as e:
        print(f"  ✓ PASS: http blocked - {str(e)[:60]}...")

    # Test 4: requests (if installed)
    print("\nTest 4: Importing requests...")
    try:
        import requests
        print("  ✗ FAIL: requests was not blocked!")
    except ImportError as e:
        print(f"  ✓ PASS: requests blocked - {str(e)[:60]}...")

    # Test 5: Network command in subprocess
    print("\nTest 5: Running curl command...")
    try:
        import subprocess
        subprocess.run(['curl', 'example.com'])
        print("  ✗ FAIL: curl was not blocked!")
    except Exception as e:
        error_msg = str(e)
        if 'blocked' in error_msg.lower() or 'network' in error_msg.lower():
            print(f"  ✓ PASS: curl blocked - {error_msg[:60]}...")
        else:
            print(f"  ? INFO: curl not available - {error_msg[:60]}...")

    print()


def main():
    print("=" * 70)
    print("Worm Python - Network Blocking Demonstration")
    print("=" * 70)
    print()

    # Check if running in Worm Python
    if os.environ.get('WORM_PYTHON') == '1':
        print("✓ Running in Worm Python - Network isolation active")
    else:
        print("⚠ WARNING: Not running in Worm Python!")
        print("  Use 'worm network_blocking_demo.py' to see full protection")
    print()

    test_allowed_operations()
    test_blocked_operations()

    print("=" * 70)
    print("Summary:")
    print("  • All standard Python features work normally")
    print("  • Network operations are comprehensively blocked")
    print("  • Your code runs safely without network access")
    print("=" * 70)


if __name__ == '__main__':
    main()
