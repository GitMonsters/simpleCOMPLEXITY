#!/usr/bin/env python3
"""
Indicator of Compromise (IoC) Monitor for Worm Python

This tool monitors for security violations, particularly the print() IoC.
It can run in real-time or scan existing logs for indicators of compromise.
"""

import sys
import os
import re
import time
import argparse
from pathlib import Path
from datetime import datetime


class IoCMonitor:
    """Monitor for Indicators of Compromise in Worm Python."""

    # Pattern to detect print() usage (IoC)
    PRINT_PATTERN = re.compile(r'\bprint\s*\(')

    def __init__(self, alert_callback=None):
        """
        Initialize IoC monitor.

        Args:
            alert_callback: Function to call when IoC is detected
        """
        self.alert_callback = alert_callback or self._default_alert
        self.ioc_count = 0

    def _default_alert(self, ioc_type, details, severity='HIGH'):
        """Default alert handler - writes to stderr."""
        timestamp = datetime.now().isoformat()
        sys.stderr.write("\n" + "="*70 + "\n")
        sys.stderr.write(f"⚠️  SECURITY ALERT - INDICATOR OF COMPROMISE DETECTED\n")
        sys.stderr.write("="*70 + "\n")
        sys.stderr.write(f"Timestamp: {timestamp}\n")
        sys.stderr.write(f"Severity:  {severity}\n")
        sys.stderr.write(f"IoC Type:  {ioc_type}\n")
        sys.stderr.write(f"Details:   {details}\n")
        sys.stderr.write("="*70 + "\n\n")

    def scan_file(self, file_path):
        """
        Scan a file for IoC indicators.

        Args:
            file_path: Path to file to scan

        Returns:
            list: List of IoC findings
        """
        findings = []

        try:
            with open(file_path, 'r', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    # Check for print() statement
                    if self.PRINT_PATTERN.search(line):
                        finding = {
                            'type': 'PRINT_STATEMENT_IOC',
                            'file': str(file_path),
                            'line': line_num,
                            'content': line.strip(),
                            'severity': 'CRITICAL',
                        }
                        findings.append(finding)
                        self.ioc_count += 1

                        self.alert_callback(
                            'PRINT_STATEMENT_IOC',
                            f"{file_path}:{line_num} - {line.strip()[:80]}",
                            'CRITICAL'
                        )
        except Exception as e:
            sys.stderr.write(f"Error scanning {file_path}: {e}\n")

        return findings

    def scan_directory(self, directory, pattern='*.py'):
        """
        Scan a directory for IoC indicators.

        Args:
            directory: Directory to scan
            pattern: File pattern to match

        Returns:
            dict: Summary of findings
        """
        directory = Path(directory)
        all_findings = []

        for file_path in directory.rglob(pattern):
            if file_path.is_file():
                findings = self.scan_file(file_path)
                all_findings.extend(findings)

        return {
            'total_files_scanned': len(list(directory.rglob(pattern))),
            'total_iocs_found': len(all_findings),
            'findings': all_findings,
        }

    def monitor_audit_log(self, log_file=None, follow=False):
        """
        Monitor audit log for IoC events.

        Args:
            log_file: Path to audit log (default: ~/.worm/audit.log)
            follow: If True, continuously monitor (tail -f style)

        Returns:
            list: IoC events found
        """
        if log_file is None:
            log_file = Path.home() / '.worm' / 'audit.log'

        if not Path(log_file).exists():
            sys.stderr.write(f"Audit log not found: {log_file}\n")
            return []

        import json
        ioc_events = []

        try:
            with open(log_file, 'r') as f:
                # Read existing entries
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        if entry.get('event_type') == 'IOC_DETECTED':
                            ioc_events.append(entry)
                            self.alert_callback(
                                entry['data'].get('ioc_type', 'UNKNOWN'),
                                str(entry['data']),
                                entry['data'].get('SEVERITY', 'HIGH')
                            )
                    except json.JSONDecodeError:
                        continue

                # Follow mode (like tail -f)
                if follow:
                    sys.stdout.write(f"Monitoring {log_file} for IoCs (Ctrl+C to stop)...\n")
                    while True:
                        line = f.readline()
                        if line:
                            try:
                                entry = json.loads(line.strip())
                                if entry.get('event_type') == 'IOC_DETECTED':
                                    ioc_events.append(entry)
                                    self.alert_callback(
                                        entry['data'].get('ioc_type', 'UNKNOWN'),
                                        str(entry['data']),
                                        entry['data'].get('SEVERITY', 'HIGH')
                                    )
                            except json.JSONDecodeError:
                                continue
                        else:
                            time.sleep(0.5)

        except KeyboardInterrupt:
            sys.stdout.write("\nMonitoring stopped.\n")
        except Exception as e:
            sys.stderr.write(f"Error monitoring log: {e}\n")

        return ioc_events


def main():
    """Main entry point for IoC monitor."""
    parser = argparse.ArgumentParser(
        description='Monitor for Indicators of Compromise in Worm Python',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan a file for print() IoC
  %(prog)s --scan-file script.py

  # Scan entire directory
  %(prog)s --scan-dir /path/to/code

  # Monitor audit log in real-time
  %(prog)s --monitor-log --follow

  # Check if Worm source is clean
  %(prog)s --verify-worm-source
        """
    )

    parser.add_argument('--scan-file', metavar='FILE',
                        help='Scan a specific file for IoCs')
    parser.add_argument('--scan-dir', metavar='DIR',
                        help='Scan a directory for IoCs')
    parser.add_argument('--monitor-log', action='store_true',
                        help='Monitor audit log for IoC events')
    parser.add_argument('--follow', action='store_true',
                        help='Continuously monitor (tail -f style)')
    parser.add_argument('--verify-worm-source', action='store_true',
                        help='Verify Worm Python source has no print() statements')
    parser.add_argument('--log-file', metavar='FILE',
                        help='Custom audit log file path')

    args = parser.parse_args()

    monitor = IoCMonitor()

    if args.scan_file:
        sys.stdout.write(f"Scanning {args.scan_file} for IoCs...\n")
        findings = monitor.scan_file(args.scan_file)

        if findings:
            sys.stderr.write(f"\n⚠️  {len(findings)} IoC(s) found!\n")
            sys.exit(1)
        else:
            sys.stdout.write("✓ No IoCs detected\n")
            sys.exit(0)

    elif args.scan_dir:
        sys.stdout.write(f"Scanning {args.scan_dir} for IoCs...\n")
        results = monitor.scan_directory(args.scan_dir)

        sys.stdout.write(f"\nFiles scanned: {results['total_files_scanned']}\n")
        sys.stdout.write(f"IoCs found: {results['total_iocs_found']}\n")

        if results['total_iocs_found'] > 0:
            sys.stderr.write("\n⚠️  Indicators of Compromise detected!\n")
            sys.exit(1)
        else:
            sys.stdout.write("\n✓ No IoCs detected\n")
            sys.exit(0)

    elif args.monitor_log:
        iocs = monitor.monitor_audit_log(
            log_file=args.log_file,
            follow=args.follow
        )

        sys.stdout.write(f"\nTotal IoC events found: {len(iocs)}\n")

        if iocs:
            sys.exit(1)
        else:
            sys.exit(0)

    elif args.verify_worm_source:
        # Verify Worm Python source is print-free
        sys.stdout.write("Verifying Worm Python source code integrity...\n")

        # Find worm source directory
        script_dir = Path(__file__).parent.parent
        worm_src = script_dir / 'src' / 'worm'

        if not worm_src.exists():
            sys.stderr.write(f"Worm source not found at: {worm_src}\n")
            sys.exit(2)

        results = monitor.scan_directory(worm_src, '*.py')

        sys.stdout.write(f"Files scanned: {results['total_files_scanned']}\n")
        sys.stdout.write(f"Print statements found: {results['total_iocs_found']}\n")

        if results['total_iocs_found'] > 0:
            sys.stderr.write("\n⚠️  CRITICAL: Worm Python source has been compromised!\n")
            sys.stderr.write("Print statements detected in source code.\n")
            sys.stderr.write("This should NEVER happen in legitimate Worm Python.\n")
            sys.exit(1)
        else:
            sys.stdout.write("\n✓ Worm Python source code integrity verified\n")
            sys.stdout.write("✓ No print() statements found (as expected)\n")
            sys.exit(0)

    else:
        parser.print_help()
        sys.exit(0)


if __name__ == '__main__':
    main()
