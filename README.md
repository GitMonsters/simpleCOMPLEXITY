# Worm Python

A security-hardened Python distribution with network isolation and vulnerability mitigations.

## Overview

Worm Python is a modified Python distribution designed for secure execution environments where network access must be strictly controlled. It maintains full Python functionality for computation, file I/O, and user interaction while blocking all network capabilities.

## Security Features

### 1. Print-Free Codebase (Breach Detection)
- **Zero `print()` Statements**: All Worm Python code uses `sys.stdout.write()` instead
- **Indicator of Compromise**: If you see `print(` in execution, the system is compromised
- **Screen Manipulation Detection**: Helps identify malicious code injecting output
- **Immediate Alert**: No false positives - legitimate Worm code never uses `print()`

### 2. Network Isolation (Multi-Layer)
- **Import Restrictions**: Socket, urllib, http, requests modules completely blocked
- **Subprocess Filtering**: Network commands (curl, wget, ssh) blocked
- **Seccomp Syscall Blocking**: Kernel-level network syscall filtering (Linux)
- **DNS Resolution Disabled**: No external DNS lookups

### 3. Resource Limits
- **CPU Time Limits**: Prevent infinite loops and DoS attacks
- **Memory Limits**: Control memory usage per script
- **File Size Limits**: Restrict maximum file creation size
- **Open Files Limits**: Limit number of concurrent open files

### 4. Restricted Builtins (Optional)
- **Block eval()**: Prevent dynamic code execution
- **Block exec()**: Disable arbitrary code execution
- **Block compile()**: Stop code object creation
- **Configurable Levels**: Strict, moderate, or minimal restrictions

### 5. Filesystem Sandboxing (Optional)
- **Read-Only Mode**: Allow only file reads, block all writes
- **Whitelist Mode**: Only access specific directories
- **Blacklist Mode**: Block access to sensitive paths

### 6. Audit Logging
- **Comprehensive Logging**: All security events logged to JSON
- **Event Types**: Blocked imports, subprocess, builtins, IoCs
- **Searchable Logs**: Query by event type, timestamp
- **SIEM Integration**: JSON format for easy ingestion

### 7. IoC Monitoring
- **Real-Time Monitoring**: Detect security violations as they occur
- **Print Statement Detection**: Immediate breach indicator
- **Alert System**: Configurable alerts for critical events
- **Source Integrity Verification**: Ensure Worm Python hasn't been modified

### What Still Works
- All standard I/O operations (print, input, file operations)
- Mathematical and scientific computing
- Data processing and manipulation
- Local file system access (with optional sandboxing)
- All non-network standard library modules

## Use Cases

Worm Python is designed for defensive security scenarios:

### Primary Use Cases
- **Untrusted Code Execution**: Code competitions, homework submissions, bug bounties
- **Sensitive Data Processing**: HIPAA, PII, financial data, classified documents
- **Educational Environments**: CS classrooms, coding bootcamps, online courses
- **Malware Analysis**: Safe detonation of suspicious scripts
- **CI/CD Security**: Testing external contributions safely
- **Air-Gapped Environments**: Government, defense, secure facilities
- **Competitive Programming**: Automated judging systems
- **Code Review**: Safe execution during security audits

See [docs/USE_CASES.md](docs/USE_CASES.md) for detailed use case documentation.

## Architecture

Worm Python implements defense-in-depth security:

1. **Import Restrictions**: Python-level module blocking
2. **Subprocess Filtering**: Command analysis and blocking
3. **Seccomp Syscalls**: Kernel-level network blocking (Linux)
4. **Resource Limits**: CPU, memory, file size restrictions
5. **Restricted Builtins**: Optional eval/exec/compile blocking
6. **Filesystem Sandbox**: Optional read-only/whitelist modes
7. **Audit Logging**: Comprehensive security event tracking
8. **IoC Detection**: Print-free codebase for breach detection

## Installation

### Quick Install

```bash
# Clone or download this repository
cd COMPLEXITY

# Install for current user
./scripts/install.sh

# Or system-wide (requires sudo)
sudo ./scripts/install.sh

# Verify installation
worm --version
worm --info
```

### Verify Integrity

```bash
# Ensure no print() statements in source (security feature)
python3 tools/ioc_monitor.py --verify-worm-source
```

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for production deployment guide.

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

## Monitoring & Security Tools

### IoC Monitor

```bash
# Verify Worm source integrity
python3 tools/ioc_monitor.py --verify-worm-source

# Scan a file for print() IoC
python3 tools/ioc_monitor.py --scan-file script.py

# Monitor audit log in real-time
python3 tools/ioc_monitor.py --monitor-log --follow
```

### Security Monitor

```bash
# Check security status
tools/worm_monitor.sh status

# Monitor in real-time
tools/worm_monitor.sh follow

# Verify source integrity
tools/worm_monitor.sh verify
```

## Testing Network Restrictions

```python
# This will fail with clear error message
import socket  # ImportError: socket module is disabled in Worm Python

# This also fails
import subprocess
subprocess.run(['curl', 'example.com'])  # NetworkCommandError

# This works fine
import sys
sys.stdout.write("Hello from Worm Python!\n")
with open("test.txt", "w") as f:
    f.write("File I/O works perfectly")
```

## Documentation

- **[Quick Start Guide](docs/QUICKSTART.md)** - Get started quickly
- **[Security Documentation](docs/SECURITY.md)** - Security model and IoC detection
- **[Use Cases](docs/USE_CASES.md)** - Intended use cases and examples
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment
- **[Examples](examples/)** - Sample scripts demonstrating features

## Project Status

**Current version**: 0.1.0-alpha
**Based on**: Python 3.x (compatible with 3.8+)

### Features
- ✅ Network isolation (import hooks + subprocess filtering + seccomp)
- ✅ Resource limits (CPU, memory, file size, open files)
- ✅ Restricted builtins (eval, exec, compile)
- ✅ Filesystem sandboxing (read-only, whitelist, blacklist)
- ✅ Audit logging (JSON format)
- ✅ IoC monitoring (print-free codebase)
- ✅ Production-ready monitoring tools

## Contributing

Worm Python is a defensive security tool. Contributions that enhance security, add defensive features, or improve documentation are welcome.

**NOT Accepted**: Changes that weaken security, remove restrictions, or enable malicious use.

## License

See LICENSE file for details.

## Security Disclosure

If you discover a way to bypass Worm Python's security features, please report it responsibly. Do not publicly disclose until a fix is available.
