"""
Seccomp-based syscall filtering for Worm Python

This module provides kernel-level network blocking using seccomp-bpf.
When enabled, the Linux kernel will block network-related system calls
at the lowest level possible.
"""

import sys
import os


def is_seccomp_available():
    """Check if seccomp is available on this system."""
    # Seccomp is Linux-only
    if sys.platform != 'linux':
        return False

    # Check if prctl is available
    try:
        import ctypes
        libc = ctypes.CDLL('libc.so.6')
        return True
    except (OSError, AttributeError):
        return False


def enable_network_blocking():
    """
    Enable seccomp filtering to block network syscalls.

    This provides kernel-level enforcement of network restrictions.
    Once enabled, it CANNOT be disabled (even by root).

    Returns:
        bool: True if seccomp was successfully enabled, False otherwise
    """
    if not is_seccomp_available():
        return False

    try:
        import ctypes
        import struct

        # Seccomp constants
        SECCOMP_MODE_FILTER = 2
        SECCOMP_RET_ALLOW = 0x7fff0000
        SECCOMP_RET_KILL = 0x00000000
        SECCOMP_RET_ERRNO = 0x00050000

        PR_SET_NO_NEW_PRIVS = 38
        PR_SET_SECCOMP = 22

        # Architecture
        AUDIT_ARCH_X86_64 = 0xc000003e

        # Network-related syscalls to block
        BLOCKED_SYSCALLS = {
            'socket': 41,
            'connect': 42,
            'accept': 43,
            'sendto': 44,
            'recvfrom': 45,
            'sendmsg': 46,
            'recvmsg': 47,
            'bind': 49,
            'listen': 50,
            'socketpair': 53,
            'setsockopt': 54,
            'getsockopt': 55,
            'accept4': 288,
            'sendmmsg': 307,
            'recvmmsg': 299,
        }

        # BPF instruction structure
        class sock_filter(ctypes.Structure):
            _fields_ = [
                ('code', ctypes.c_uint16),
                ('jt', ctypes.c_uint8),
                ('jf', ctypes.c_uint8),
                ('k', ctypes.c_uint32),
            ]

        class sock_fprog(ctypes.Structure):
            _fields_ = [
                ('len', ctypes.c_uint16),
                ('filter', ctypes.POINTER(sock_filter)),
            ]

        # Build BPF program
        # This is a simplified filter that blocks the most critical syscalls
        filters = []

        # Load architecture
        filters.append(sock_filter(0x20, 0, 0, 4))  # LD [4] (arch)

        # Check if x86_64
        filters.append(sock_filter(0x15, 0, len(BLOCKED_SYSCALLS) + 1, AUDIT_ARCH_X86_64))

        # Load syscall number
        filters.append(sock_filter(0x20, 0, 0, 0))  # LD [0] (syscall nr)

        # Check each blocked syscall
        remaining = len(BLOCKED_SYSCALLS)
        for name, nr in BLOCKED_SYSCALLS.items():
            remaining -= 1
            # If syscall matches, return ERRNO
            filters.append(sock_filter(0x15, 0, remaining, nr))

        # If we get here, syscall is allowed
        filters.append(sock_filter(0x06, 0, 0, SECCOMP_RET_ERRNO | 1))  # Return EPERM
        filters.append(sock_filter(0x06, 0, 0, SECCOMP_RET_ALLOW))  # Allow

        # Create filter array
        filter_array = (sock_filter * len(filters))(*filters)
        prog = sock_fprog(len(filters), filter_array)

        # Load libc
        libc = ctypes.CDLL('libc.so.6')

        # Set NO_NEW_PRIVS (required for unprivileged seccomp)
        ret = libc.prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)
        if ret != 0:
            return False

        # Enable seccomp filter
        ret = libc.prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, ctypes.byref(prog), 0, 0)
        if ret != 0:
            return False

        return True

    except Exception as e:
        # Seccomp failed, but we continue (Python-level restrictions still active)
        return False


def get_status():
    """
    Get seccomp status information.

    Returns:
        dict: Status information
    """
    status = {
        'available': is_seccomp_available(),
        'platform': sys.platform,
        'enabled': False,
    }

    if sys.platform == 'linux':
        try:
            with open('/proc/self/status', 'r') as f:
                for line in f:
                    if line.startswith('Seccomp:'):
                        seccomp_mode = line.split(':')[1].strip()
                        status['enabled'] = seccomp_mode != '0'
                        status['mode'] = seccomp_mode
                        break
        except:
            pass

    return status


if __name__ == '__main__':
    sys.stdout.write("Testing seccomp network blocking...\n")

    status = get_status()
    sys.stdout.write(f"Platform: {status['platform']}\n")
    sys.stdout.write(f"Seccomp available: {status['available']}\n")

    if status['available']:
        sys.stdout.write("\nAttempting to enable seccomp filtering...\n")
        result = enable_network_blocking()

        if result:
            sys.stdout.write("✓ Seccomp filtering enabled successfully\n")

            # Verify it's active
            new_status = get_status()
            sys.stdout.write(f"✓ Seccomp mode: {new_status.get('mode', 'unknown')}\n")

            # Try to create a socket (should fail)
            sys.stdout.write("\nTesting network blocking...\n")
            try:
                import socket
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sys.stdout.write("ERROR: Socket creation was not blocked!\n")
            except Exception as e:
                sys.stdout.write(f"✓ Socket creation blocked: {type(e).__name__}\n")
        else:
            sys.stdout.write("⚠ Seccomp filtering could not be enabled\n")
            sys.stdout.write("  (This is normal on non-Linux systems or in containers)\n")
    else:
        sys.stdout.write("\n⚠ Seccomp not available on this platform\n")
        sys.stdout.write("  (Python-level restrictions are still active)\n")
