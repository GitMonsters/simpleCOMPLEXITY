"""
Audit logging for Worm Python

Tracks all security-relevant events including blocked operations,
resource usage, and potential security violations.
"""

import sys
import os
import time
import json
from datetime import datetime
from pathlib import Path


class AuditLogger:
    """
    Audit logger for tracking security events.

    Logs are written in JSON format for easy parsing and analysis.
    """

    def __init__(self, log_file=None, enabled=True):
        """
        Initialize audit logger.

        Args:
            log_file: Path to log file (default: ~/.worm/audit.log)
            enabled: Whether logging is enabled
        """
        self.enabled = enabled

        if log_file is None:
            # Default log location
            worm_dir = Path.home() / '.worm'
            worm_dir.mkdir(exist_ok=True)
            log_file = worm_dir / 'audit.log'

        self.log_file = str(log_file)
        self.session_id = f"{os.getpid()}_{int(time.time())}"

    def _write_log(self, event_type, data):
        """Write a log entry."""
        if not self.enabled:
            return

        entry = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'session_id': self.session_id,
            'pid': os.getpid(),
            'event_type': event_type,
            'data': data,
        }

        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception as e:
            # Logging failed, but don't crash the program
            sys.stderr.write(f"Audit log write failed: {e}\n")

    def log_blocked_import(self, module_name, caller_file=None):
        """Log a blocked module import."""
        self._write_log('blocked_import', {
            'module': module_name,
            'caller': caller_file,
        })

    def log_blocked_subprocess(self, command, reason):
        """Log a blocked subprocess command."""
        self._write_log('blocked_subprocess', {
            'command': command if isinstance(command, str) else ' '.join(command),
            'reason': reason,
        })

    def log_restricted_builtin(self, builtin_name):
        """Log attempt to use restricted builtin."""
        self._write_log('restricted_builtin', {
            'builtin': builtin_name,
        })

    def log_resource_limit_hit(self, resource_type, limit_value):
        """Log resource limit being hit."""
        self._write_log('resource_limit_hit', {
            'resource': resource_type,
            'limit': limit_value,
        })

    def log_session_start(self, script_path=None, args=None):
        """Log session start."""
        self._write_log('session_start', {
            'script': script_path,
            'args': args,
            'cwd': os.getcwd(),
        })

    def log_session_end(self, exit_code=0):
        """Log session end."""
        self._write_log('session_end', {
            'exit_code': exit_code,
        })

    def log_ioc_detected(self, ioc_type, details):
        """
        Log Indicator of Compromise detection.

        This is for critical security events like print() detection.
        """
        self._write_log('IOC_DETECTED', {
            'ioc_type': ioc_type,
            'details': details,
            'SEVERITY': 'CRITICAL',
        })

    def log_custom(self, event_type, data):
        """Log a custom event."""
        self._write_log(event_type, data)


# Global audit logger instance
_audit_logger = None


def get_audit_logger():
    """Get the global audit logger instance."""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger


def enable_audit_logging(log_file=None):
    """
    Enable audit logging globally.

    Args:
        log_file: Optional custom log file path

    Returns:
        AuditLogger: The global logger instance
    """
    global _audit_logger
    _audit_logger = AuditLogger(log_file=log_file, enabled=True)
    return _audit_logger


def disable_audit_logging():
    """Disable audit logging."""
    global _audit_logger
    if _audit_logger:
        _audit_logger.enabled = False


def read_audit_log(log_file=None, limit=None):
    """
    Read audit log entries.

    Args:
        log_file: Path to log file (default: ~/.worm/audit.log)
        limit: Maximum number of entries to return (most recent)

    Returns:
        list: List of log entries (dicts)
    """
    if log_file is None:
        log_file = Path.home() / '.worm' / 'audit.log'

    entries = []

    try:
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    entries.append(entry)
                except json.JSONDecodeError:
                    continue

        # Return most recent entries if limit specified
        if limit:
            entries = entries[-limit:]

    except FileNotFoundError:
        pass

    return entries


def search_audit_log(event_type=None, since=None, log_file=None):
    """
    Search audit log for specific events.

    Args:
        event_type: Filter by event type
        since: ISO timestamp to search from
        log_file: Path to log file

    Returns:
        list: Matching log entries
    """
    entries = read_audit_log(log_file=log_file)

    results = []
    for entry in entries:
        # Filter by event type
        if event_type and entry.get('event_type') != event_type:
            continue

        # Filter by timestamp
        if since and entry.get('timestamp', '') < since:
            continue

        results.append(entry)

    return results


if __name__ == '__main__':
    sys.stdout.write("Testing audit logging...\n\n")

    # Create test logger with temp file
    import tempfile
    temp_log = tempfile.mktemp(suffix='.log')

    logger = AuditLogger(log_file=temp_log)
    sys.stdout.write(f"Log file: {temp_log}\n\n")

    # Log various events
    sys.stdout.write("Logging test events...\n")
    logger.log_session_start('/test/script.py', ['arg1', 'arg2'])
    logger.log_blocked_import('socket')
    logger.log_blocked_subprocess(['curl', 'example.com'], 'network command')
    logger.log_restricted_builtin('eval')
    logger.log_ioc_detected('print_statement', 'print() detected in execution')
    logger.log_session_end(0)

    sys.stdout.write("✓ Events logged\n\n")

    # Read back logs
    sys.stdout.write("Reading audit log:\n")
    entries = read_audit_log(log_file=temp_log)

    for entry in entries:
        sys.stdout.write(f"  [{entry['event_type']}] {entry['data']}\n")

    sys.stdout.write(f"\n✓ Total entries: {len(entries)}\n")

    # Search for IOCs
    sys.stdout.write("\nSearching for IOC events:\n")
    iocs = search_audit_log(event_type='IOC_DETECTED', log_file=temp_log)
    for ioc in iocs:
        sys.stdout.write(f"  ⚠ CRITICAL: {ioc['data']}\n")

    # Cleanup
    os.unlink(temp_log)
    sys.stdout.write("\n✓ Audit logging test complete\n")
