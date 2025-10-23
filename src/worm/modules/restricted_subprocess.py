"""
Restricted subprocess module for Worm Python

This module wraps the standard subprocess module to prevent execution
of network-related commands.
"""

import subprocess as _real_subprocess
import shlex


# Network-related commands that should be blocked
BLOCKED_COMMANDS = {
    'curl', 'wget', 'nc', 'netcat', 'telnet', 'ssh', 'scp', 'sftp',
    'ftp', 'ping', 'nmap', 'nslookup', 'dig', 'host', 'traceroute',
    'tracert', 'route', 'netstat', 'ss', 'ip', 'ifconfig', 'tcpdump',
    'wireshark', 'iptables', 'firewall-cmd', 'ufw'
}

# Command patterns that indicate network operations
BLOCKED_PATTERNS = [
    '://',  # URLs
    'http', 'https', 'ftp', 'ssh',
]


class NetworkCommandError(Exception):
    """Raised when attempting to execute a network-related command."""
    pass


def _check_command_safety(cmd):
    """
    Check if a command is safe to execute (doesn't involve network access).

    Args:
        cmd: Command as string or list

    Raises:
        NetworkCommandError: If command involves network operations
    """
    # Convert to string for analysis
    if isinstance(cmd, (list, tuple)):
        cmd_str = ' '.join(str(x) for x in cmd)
        base_cmd = str(cmd[0]).split('/')[-1] if cmd else ''
    else:
        cmd_str = str(cmd)
        try:
            parts = shlex.split(cmd_str)
            base_cmd = parts[0].split('/')[-1] if parts else ''
        except:
            base_cmd = cmd_str.split()[0] if cmd_str.split() else ''

    # Check base command
    if base_cmd in BLOCKED_COMMANDS:
        raise NetworkCommandError(
            f"Command '{base_cmd}' is blocked in Worm Python (network command). "
            f"Network operations are disabled for security."
        )

    # Check for URL patterns
    for pattern in BLOCKED_PATTERNS:
        if pattern in cmd_str.lower():
            raise NetworkCommandError(
                f"Command contains blocked pattern '{pattern}' (likely network operation). "
                f"Network operations are disabled in Worm Python."
            )


# Wrap subprocess functions with safety checks
def run(*args, **kwargs):
    """Safe wrapper for subprocess.run()"""
    if args:
        _check_command_safety(args[0])
    return _real_subprocess.run(*args, **kwargs)


def call(*args, **kwargs):
    """Safe wrapper for subprocess.call()"""
    if args:
        _check_command_safety(args[0])
    return _real_subprocess.call(*args, **kwargs)


def check_call(*args, **kwargs):
    """Safe wrapper for subprocess.check_call()"""
    if args:
        _check_command_safety(args[0])
    return _real_subprocess.check_call(*args, **kwargs)


def check_output(*args, **kwargs):
    """Safe wrapper for subprocess.check_output()"""
    if args:
        _check_command_safety(args[0])
    return _real_subprocess.check_output(*args, **kwargs)


def Popen(*args, **kwargs):
    """Safe wrapper for subprocess.Popen()"""
    if args:
        _check_command_safety(args[0])
    return _real_subprocess.Popen(*args, **kwargs)


# Re-export safe constants and exceptions
PIPE = _real_subprocess.PIPE
STDOUT = _real_subprocess.STDOUT
DEVNULL = _real_subprocess.DEVNULL
CalledProcessError = _real_subprocess.CalledProcessError
TimeoutExpired = _real_subprocess.TimeoutExpired


if __name__ == '__main__':
    print("Testing restricted subprocess module...")

    # Test allowed command
    try:
        result = run(['echo', 'Hello from Worm Python'], capture_output=True, text=True)
        print(f"✓ Allowed command worked: {result.stdout.strip()}")
    except Exception as e:
        print(f"ERROR: Allowed command failed: {e}")

    # Test blocked command
    try:
        run(['curl', 'example.com'])
        print("ERROR: curl was not blocked!")
    except NetworkCommandError as e:
        print(f"✓ Network command blocked: {type(e).__name__}")

    # Test URL detection
    try:
        run(['wget', 'http://example.com'])
        print("ERROR: wget with URL was not blocked!")
    except NetworkCommandError as e:
        print(f"✓ URL pattern blocked: {type(e).__name__}")
