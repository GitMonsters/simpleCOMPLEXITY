"""
Resource limits for Worm Python

Implements CPU time, memory, and other resource restrictions
to prevent DoS attacks and resource exhaustion.
"""

import sys
import os
import signal


class ResourceLimitError(Exception):
    """Raised when a resource limit is exceeded."""
    pass


def set_cpu_limit(seconds):
    """
    Set CPU time limit in seconds.

    Args:
        seconds: Maximum CPU time allowed (0 = unlimited)

    Returns:
        bool: True if limit was set successfully
    """
    if seconds <= 0:
        return False

    try:
        import resource
        resource.setrlimit(resource.RLIMIT_CPU, (seconds, seconds))
        return True
    except (ImportError, OSError, ValueError):
        # resource module not available or operation not permitted
        # Fall back to signal-based timeout
        try:
            def timeout_handler(signum, frame):
                raise ResourceLimitError(
                    f"CPU time limit exceeded ({seconds} seconds). "
                    "Script terminated for security."
                )

            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(seconds)
            return True
        except:
            return False


def set_memory_limit(megabytes):
    """
    Set memory limit in megabytes.

    Args:
        megabytes: Maximum memory in MB (0 = unlimited)

    Returns:
        bool: True if limit was set successfully
    """
    if megabytes <= 0:
        return False

    try:
        import resource
        bytes_limit = megabytes * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (bytes_limit, bytes_limit))
        return True
    except (ImportError, OSError, ValueError):
        return False


def set_file_size_limit(megabytes):
    """
    Set maximum file size that can be created.

    Args:
        megabytes: Maximum file size in MB (0 = unlimited)

    Returns:
        bool: True if limit was set successfully
    """
    if megabytes <= 0:
        return False

    try:
        import resource
        bytes_limit = megabytes * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_FSIZE, (bytes_limit, bytes_limit))
        return True
    except (ImportError, OSError, ValueError):
        return False


def set_open_files_limit(max_files):
    """
    Set maximum number of open files.

    Args:
        max_files: Maximum number of files (0 = unlimited)

    Returns:
        bool: True if limit was set successfully
    """
    if max_files <= 0:
        return False

    try:
        import resource
        resource.setrlimit(resource.RLIMIT_NOFILE, (max_files, max_files))
        return True
    except (ImportError, OSError, ValueError):
        return False


def set_standard_limits(profile='moderate'):
    """
    Apply a standard set of resource limits.

    Args:
        profile: Security profile to use
            - 'strict': Very restrictive (competitions, untrusted code)
            - 'moderate': Balanced (general use)
            - 'relaxed': Minimal restrictions (trusted code)

    Returns:
        dict: Status of each limit applied
    """
    results = {}

    if profile == 'strict':
        results['cpu'] = set_cpu_limit(30)  # 30 seconds
        results['memory'] = set_memory_limit(512)  # 512 MB
        results['file_size'] = set_file_size_limit(10)  # 10 MB
        results['open_files'] = set_open_files_limit(100)  # 100 files

    elif profile == 'moderate':
        results['cpu'] = set_cpu_limit(300)  # 5 minutes
        results['memory'] = set_memory_limit(2048)  # 2 GB
        results['file_size'] = set_file_size_limit(100)  # 100 MB
        results['open_files'] = set_open_files_limit(1000)  # 1000 files

    elif profile == 'relaxed':
        results['cpu'] = set_cpu_limit(3600)  # 1 hour
        results['memory'] = set_memory_limit(4096)  # 4 GB
        results['file_size'] = set_file_size_limit(1024)  # 1 GB
        results['open_files'] = set_open_files_limit(10000)  # 10000 files

    return results


def get_current_usage():
    """
    Get current resource usage.

    Returns:
        dict: Current resource usage statistics
    """
    usage = {}

    try:
        import resource

        # CPU time
        rusage = resource.getrusage(resource.RUSAGE_SELF)
        usage['cpu_user'] = rusage.ru_utime
        usage['cpu_system'] = rusage.ru_stime
        usage['cpu_total'] = rusage.ru_utime + rusage.ru_stime

        # Memory
        usage['max_rss_mb'] = rusage.ru_maxrss / 1024  # Convert to MB

        # Get current limits
        try:
            cpu_soft, cpu_hard = resource.getrlimit(resource.RLIMIT_CPU)
            usage['cpu_limit'] = cpu_soft if cpu_soft != resource.RLIM_INFINITY else None
        except:
            usage['cpu_limit'] = None

        try:
            mem_soft, mem_hard = resource.getrlimit(resource.RLIMIT_AS)
            usage['memory_limit_mb'] = (mem_soft / 1024 / 1024) if mem_soft != resource.RLIM_INFINITY else None
        except:
            usage['memory_limit_mb'] = None

    except ImportError:
        # resource module not available
        pass

    return usage


if __name__ == '__main__':
    sys.stdout.write("Testing resource limits...\n\n")

    # Show current usage
    usage = get_current_usage()
    sys.stdout.write("Current resource usage:\n")
    for key, value in usage.items():
        if value is not None:
            sys.stdout.write(f"  {key}: {value}\n")

    sys.stdout.write("\nApplying 'moderate' resource limits...\n")
    results = set_standard_limits('moderate')

    for limit, success in results.items():
        status = "✓" if success else "⚠"
        sys.stdout.write(f"  {status} {limit}: {'set' if success else 'not available'}\n")

    # Show updated usage
    sys.stdout.write("\nUpdated limits:\n")
    usage = get_current_usage()
    if usage.get('cpu_limit'):
        sys.stdout.write(f"  CPU limit: {usage['cpu_limit']} seconds\n")
    if usage.get('memory_limit_mb'):
        sys.stdout.write(f"  Memory limit: {usage['memory_limit_mb']:.0f} MB\n")

    sys.stdout.write("\n✓ Resource limits tested\n")
