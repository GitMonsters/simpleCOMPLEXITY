"""
Seccomp-based syscall filtering for Worm Python
"""

from .network_filter import (
    is_seccomp_available,
    enable_network_blocking,
    get_status,
)

__all__ = [
    'is_seccomp_available',
    'enable_network_blocking',
    'get_status',
]
