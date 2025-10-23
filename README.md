# Worm Python

A security-hardened Python distribution with network isolation and vulnerability mitigations.

## Overview

Worm Python is a modified Python distribution designed for secure execution environments where network access must be strictly controlled. It maintains full Python functionality for computation, file I/O, and user interaction while blocking all network capabilities.

## Security Features

### Print-Free Codebase (Breach Detection)
- **Zero `print()` Statements**: All Worm Python code uses `sys.stdout.write()` instead
- **Indicator of Compromise**: If you see `print(` in execution, the system is compromised
- **Screen Manipulation Detection**: Helps identify malicious code injecting output
- **Immediate Alert**: No false positives - legitimate Worm code never uses `print()`

### Network Isolation
- **No TCP/UDP Socket Access**: Socket module is completely disabled
- **HTTP/HTTPS Blocked**: All web request libraries are restricted
- **DNS Resolution Disabled**: No external DNS lookups
- **Subprocess Network Restrictions**: Cannot execute network commands

### Vulnerability Mitigations
- Patches for known Python CVEs
- Restricted use of dangerous functions (eval, exec, pickle)
- Syscall filtering via seccomp
- Import restrictions on dangerous modules

### What Still Works
- All standard I/O operations (print, input, file operations)
- Mathematical and scientific computing
- Data processing and manipulation
- Local file system access (with optional sandboxing)
- All non-network standard library modules

## Use Cases

- Executing untrusted Python scripts safely
- Sandboxed code execution environments
- Educational environments requiring network isolation
- Processing sensitive data without exfiltration risk
- Running user-submitted code in competitions/challenges

## Architecture

Worm Python uses multiple defense layers:

1. **Compile-time restrictions**: CPython source modifications
2. **Runtime enforcement**: Custom import hooks and module replacements
3. **Syscall filtering**: Seccomp-based network syscall blocking
4. **Documentation**: Clear audit trail of all security modifications

## Installation

```bash
# Build from source
./build.sh

# Install
sudo make install

# Verify installation
worm --version
```

## Usage

Use `worm` exactly like you would use `python`:

```bash
# Run a script
worm script.py

# Interactive REPL
worm

# Run module
worm -m module_name
```

## Testing Network Restrictions

```python
# This will fail with clear error message
import socket  # ImportError: socket module is disabled in Worm Python

# This works fine
print("Hello from Worm Python!")
with open("test.txt", "w") as f:
    f.write("File I/O works perfectly")
```

## Project Status

Current version: 0.1.0-alpha
Based on: CPython 3.12.x

## License

See LICENSE file for details.

## Security Disclosure

If you discover a security vulnerability in Worm Python, please report it responsibly.
