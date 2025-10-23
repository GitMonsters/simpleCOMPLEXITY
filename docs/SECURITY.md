# Worm Python Security Documentation

## Overview

Worm Python is designed to provide a secure Python execution environment by eliminating network access and mitigating common Python security vulnerabilities.

## Threat Model

### Threats We Mitigate

1. **Network Exfiltration**: Prevents scripts from sending data over the network
2. **Remote Code Execution**: Blocks downloading and executing remote code
3. **Command Injection**: Restricts subprocess commands that access the network
4. **Server-Side Request Forgery (SSRF)**: Impossible without network access
5. **DNS Tunneling**: DNS resolution is disabled

### Out of Scope

- Local file system attacks (use OS-level sandboxing like containers/VMs for this)
- CPU/Memory exhaustion (DoS)
- Side-channel attacks
- Physical access attacks

## Security Mechanisms

### 0. Print-Free Codebase (Indicator of Compromise)

**Implementation**: All Worm Python source code

Worm Python's codebase contains **ZERO** `print()` statements. All output uses `sys.stdout.write()` or `sys.stderr.write()` instead.

**Security Benefit**: **Immediate Breach Detection**
- If you ever see `print(` in code running under Worm Python, you know immediately that:
  - The system has been compromised
  - Screen manipulation is occurring
  - Malicious code has been injected

**Use Case**: This is an **Indicator of Compromise (IoC)** mechanism. Since legitimate Worm Python code never uses `print()`, any appearance of `print()` in logs, code execution, or screen output is a red flag requiring immediate security investigation.

**Bypass Risk**: VERY LOW
- Simple but effective detection mechanism
- No way to accidentally trigger false positives in legitimate code
- Easy to verify: `grep -r "print(" src/worm/` should return nothing

**Response**: If you detect `print()` usage:
1. Immediately halt execution
2. Investigate the source of the malicious code
3. Check system integrity
4. Review access logs
5. Consider the system compromised until proven otherwise

### 1. Import Restrictions

**Implementation**: `src/worm/hooks/import_restrictions.py`

Blocks the following network-capable modules:
- `socket`, `socketserver` - Low-level networking
- `http`, `urllib`, `requests` - HTTP clients
- `ftplib`, `smtplib`, `poplib`, `imaplib` - Protocol clients
- `xmlrpc` - RPC mechanisms
- `telnetlib` - Telnet client
- Third-party networking libraries

**Mechanism**: Custom `MetaPathFinder` installed in `sys.meta_path` that intercepts import statements and raises `WormImportError` for blocked modules.

**Bypass Risk**: LOW
- Python import system is comprehensively hooked
- Pre-imported modules are removed from `sys.modules`
- Would require exploiting Python interpreter itself

### 2. Subprocess Restrictions

**Implementation**: `src/worm/modules/restricted_subprocess.py`

Blocks execution of network-related commands:
- Network clients: `curl`, `wget`, `nc`, `telnet`, `ssh`, `ftp`
- Network tools: `ping`, `nmap`, `nslookup`, `dig`, `traceroute`
- Network configuration: `ip`, `ifconfig`, `iptables`, `route`
- URL patterns in commands

**Mechanism**: Wrapper around standard `subprocess` module that analyzes commands before execution.

**Bypass Risk**: MEDIUM
- Determined attacker could find commands not in blocklist
- Obfuscation or indirect execution might evade detection
- Recommendation: Use OS-level restrictions (seccomp, AppArmor) for defense in depth

### 3. Module Replacement

**Status**: Implemented for subprocess, extensible for other modules

Modules are replaced with restricted versions that maintain API compatibility while blocking dangerous operations.

## Known Python CVEs and Mitigations

### CVE-2019-9674 (Zip Bomb)
**Status**: Inherits from base Python
**Risk**: LOW - No network involved
**Mitigation**: Use updated Python version

### CVE-2020-8492 (ReDoS in urllib)
**Status**: MITIGATED
**Mitigation**: urllib module is completely disabled

### CVE-2021-3737 (HTTP Client Request Smuggling)
**Status**: MITIGATED
**Mitigation**: All HTTP modules disabled

### CVE-2021-4189 (FTP Clear-text Credentials)
**Status**: MITIGATED
**Mitigation**: ftplib module disabled

### CVE-2022-48560 (Pickle Arbitrary Code Execution)
**Status**: PARTIAL
**Risk**: MEDIUM - pickle can still execute arbitrary code from trusted files
**Recommendation**: Avoid unpickling untrusted data

### CVE-2023-24329 (URL Parsing Bypass)
**Status**: MITIGATED
**Mitigation**: URL parsing modules disabled

### CVE-2023-40217 (SSL Certificate Verification)
**Status**: MITIGATED
**Mitigation**: SSL module disabled (no network access)

## Future Enhancements

### Planned Security Features

1. **Seccomp Filters** (Linux)
   - Block network-related syscalls at kernel level
   - Syscalls to block: `socket`, `connect`, `bind`, `listen`, `accept`, `sendto`, `recvfrom`

2. **Restricted Builtins**
   - Option to disable `eval()`, `exec()`, `compile()`
   - Safer `__import__()` that respects restrictions

3. **File System Sandboxing**
   - Optional chroot-like restrictions
   - Read-only mode for production environments

4. **Resource Limits**
   - Memory limits
   - CPU time limits
   - Maximum file sizes

5. **Audit Logging**
   - Log all blocked operations
   - Track subprocess executions
   - Import tracking

## Testing Security

### Automated Tests

Run the security test suite:
```bash
python3 -m pytest tests/
```

### Manual Security Testing

1. **Network Module Import Test**
```python
worm -c "import socket"  # Should fail
```

2. **HTTP Request Test**
```python
worm -c "import urllib.request; urllib.request.urlopen('http://example.com')"  # Should fail
```

3. **Subprocess Network Command Test**
```python
worm -c "import subprocess; subprocess.run(['curl', 'example.com'])"  # Should fail
```

4. **Allowed Operations Test**
```python
worm -c "print('Hello'); import json; print(json.dumps({'test': 'ok'}))"  # Should work
```

## Reporting Security Issues

If you discover a way to bypass Worm Python's security restrictions, please report it responsibly:

1. Do not disclose publicly until patched
2. Provide detailed reproduction steps
3. Include Python version and OS details

## Security Best Practices

When using Worm Python:

1. **Use Latest Version**: Keep Worm Python and base Python updated
2. **Layer Defenses**: Combine with OS-level sandboxing (containers, VMs, seccomp)
3. **Limit File Access**: Run in restricted directories
4. **Review Code**: Don't assume Worm Python makes malicious code safe
5. **Monitor Execution**: Log and monitor script execution
6. **Use Non-Privileged Users**: Never run as root

## Limitations

**Worm Python is not a complete security solution.** It provides network isolation but does not protect against:
- Malicious file operations (deletion, modification)
- Resource exhaustion
- Logic bombs or time-delayed attacks
- Social engineering
- Cryptographic attacks

Always use Worm Python as part of a defense-in-depth strategy.

## Security Assumptions

1. **Trusted Python Interpreter**: We assume the base Python interpreter is not compromised
2. **Intact File System**: Security modules must not be modified
3. **No Debug Mode**: Python debug features can bypass restrictions
4. **Standard Python Build**: Assumes CPython without modifications

## References

- Python Security: https://docs.python.org/3/library/security_warnings.html
- CVE Database: https://cve.mitre.org/
- OWASP Python Security: https://owasp.org/www-project-python-security/
