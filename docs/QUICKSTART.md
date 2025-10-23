# Worm Python Quick Start Guide

## Installation

### From Source

```bash
# Clone or download the repository
cd COMPLEXITY

# Install (user installation)
./scripts/install.sh

# Or install system-wide (requires sudo)
sudo ./scripts/install.sh
```

### Verify Installation

```bash
worm --version
worm --info
```

## Basic Usage

### Interactive REPL

Start an interactive Python session:

```bash
worm
```

You'll see:
```
Worm Python 0.1.0-alpha (Security Hardened)
Based on Python 3.x
Type "help", "copyright", "credits" or "license" for more information.
Network access is DISABLED in this Python distribution.

>>>
```

### Run a Script

```bash
worm script.py
```

### Execute Code Directly

```bash
worm -c "print('Hello from Worm!')"
```

### Run a Module

```bash
worm -m json.tool < data.json
```

## What Works

Everything in standard Python **except** network access:

```python
# ✓ All these work perfectly:
import json
import math
import datetime
import os
import sys
import re
import sqlite3
import csv
# ... and most other standard library modules

# File I/O works
with open('file.txt', 'w') as f:
    f.write('Hello')

# Subprocess with safe commands works
import subprocess
subprocess.run(['ls', '-la'])
subprocess.run(['python3', 'script.py'])
```

## What's Blocked

All network operations are blocked:

```python
# ✗ These will fail with clear error messages:
import socket          # Blocked
import urllib.request  # Blocked
import http.client     # Blocked
import requests        # Blocked (if installed)
import ftplib          # Blocked

# Network commands in subprocess are blocked
import subprocess
subprocess.run(['curl', 'example.com'])  # Blocked
subprocess.run(['wget', 'http://...'])    # Blocked
subprocess.run(['ping', 'example.com'])   # Blocked
```

## Example Use Cases

### 1. Running Untrusted Scripts

```bash
# Safely execute a user-submitted script
worm user_script.py
```

The script can't:
- Exfiltrate data over the network
- Download malicious code
- Connect to command & control servers

### 2. Data Processing

```bash
# Process sensitive data without risk of exfiltration
worm process_data.py input.csv output.csv
```

### 3. Code Challenges

```bash
# Run competition submissions safely
worm --timeout 10 submission.py < test_input.txt
```

### 4. Educational Environments

```bash
# Students can run code without network access concerns
worm student_homework.py
```

## Example Scripts

### Example 1: Data Analysis (examples/data_analysis.py)

```python
import json
import csv
from collections import Counter

# Read data
with open('data.csv', 'r') as f:
    reader = csv.DictReader(f)
    data = list(reader)

# Analyze
counter = Counter(row['category'] for row in data)
print(json.dumps(dict(counter), indent=2))

# Write results
with open('results.json', 'w') as f:
    json.dump(dict(counter), f, indent=2)
```

### Example 2: Mathematical Computation

```python
import math
import statistics

# Worm Python is perfect for mathematical computations
numbers = [1, 2, 3, 4, 5, 10, 20, 30]

print(f"Mean: {statistics.mean(numbers)}")
print(f"Median: {statistics.median(numbers)}")
print(f"Std Dev: {statistics.stdev(numbers)}")
print(f"Geometric mean: {math.prod(numbers) ** (1/len(numbers))}")
```

### Example 3: File Processing

```python
import os
import glob

# Process all text files in a directory
for filepath in glob.glob('*.txt'):
    with open(filepath, 'r') as f:
        content = f.read()

    # Process content
    word_count = len(content.split())
    line_count = len(content.splitlines())

    print(f"{filepath}: {line_count} lines, {word_count} words")
```

## Environment Detection

Scripts can detect if they're running in Worm Python:

```python
import os

if os.environ.get('WORM_PYTHON') == '1':
    print("Running in Worm Python - network disabled")
else:
    print("Running in standard Python")
```

## Troubleshooting

### "worm: command not found"

Add the bin directory to your PATH:

```bash
# For user installation
export PATH="$HOME/.local/bin:$PATH"

# Add to ~/.bashrc or ~/.zshrc for persistence
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

### Module Import Errors

If you get "Module 'X' is disabled" error:
- This is intentional - the module provides network access
- Use Worm Python for its intended purpose (network isolation)
- If you need network access, use standard Python

### Permission Denied

For system-wide installation:
```bash
sudo ./scripts/install.sh
```

## Uninstallation

```bash
# User installation
./scripts/uninstall.sh

# System-wide installation
sudo ./scripts/uninstall.sh
```

## Next Steps

- Read [SECURITY.md](SECURITY.md) to understand the security model
- Check out example scripts in the `examples/` directory
- Run the test suite: `./scripts/run_tests.sh`

## Getting Help

```bash
worm --help       # Show usage information
worm --info       # Show security features
worm --version    # Show version
```

For issues or questions, consult the README.md or SECURITY.md documentation.
