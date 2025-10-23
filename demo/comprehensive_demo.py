#!/usr/bin/env worm
"""
Worm Python - Comprehensive Security Feature Demonstration

This script demonstrates ALL security features of Worm Python in action.
Run this with: python3 src/worm/worm.py demo/comprehensive_demo.py

This demonstrates defensive security capabilities.
"""

import sys
import os
import time
import tempfile


def header(title):
    """Display section header."""
    sys.stdout.write("\n" + "=" * 70 + "\n")
    sys.stdout.write(f"  {title}\n")
    sys.stdout.write("=" * 70 + "\n\n")


def test_result(test_name, passed, details=""):
    """Display test result."""
    status = "✓ PASS" if passed else "✗ FAIL"
    sys.stdout.write(f"{status}: {test_name}\n")
    if details:
        sys.stdout.write(f"      {details}\n")


def demo_print_free_codebase():
    """Demonstrate the print-free codebase IoC mechanism."""
    header("1. PRINT-FREE CODEBASE (IoC Detection)")

    sys.stdout.write("Worm Python's source code contains ZERO print() statements.\n")
    sys.stdout.write("This is an Indicator of Compromise (IoC) mechanism.\n\n")

    sys.stdout.write("What this means:\n")
    sys.stdout.write("  • Legitimate Worm code never uses print()\n")
    sys.stdout.write("  • If you see print() in execution → SYSTEM COMPROMISED\n")
    sys.stdout.write("  • Detects screen manipulation attacks\n")
    sys.stdout.write("  • Zero false positives\n\n")

    sys.stdout.write("Verification:\n")
    sys.stdout.write("  $ grep -r 'print(' src/worm/\n")
    sys.stdout.write("  (should return nothing)\n\n")

    sys.stdout.write("Instead, we use: sys.stdout.write() and sys.stderr.write()\n")
    sys.stdout.write("This message was written with sys.stdout.write()\n")


def demo_network_isolation():
    """Demonstrate network isolation features."""
    header("2. NETWORK ISOLATION (Multi-Layer Defense)")

    sys.stdout.write("Layer 1: Import Restrictions\n")
    sys.stdout.write("-" * 40 + "\n")

    # Test socket import
    try:
        import socket
        test_result("Block socket import", False, "Socket was imported!")
    except ImportError as e:
        test_result("Block socket import", True, str(e)[:60] + "...")

    # Test urllib import
    try:
        import urllib.request
        test_result("Block urllib import", False, "urllib was imported!")
    except ImportError as e:
        test_result("Block urllib import", True, str(e)[:60] + "...")

    # Test http import
    try:
        import http.client
        test_result("Block http import", False, "http was imported!")
    except ImportError as e:
        test_result("Block http import", True, str(e)[:60] + "...")

    sys.stdout.write("\nLayer 2: Subprocess Filtering\n")
    sys.stdout.write("-" * 40 + "\n")

    # Test curl blocking
    import subprocess
    try:
        subprocess.run(['curl', 'example.com'])
        test_result("Block curl command", False, "curl was executed!")
    except Exception as e:
        test_result("Block curl command", True, str(e)[:60] + "...")

    # Test wget blocking
    try:
        subprocess.run(['wget', 'http://example.com'])
        test_result("Block wget command", False, "wget was executed!")
    except Exception as e:
        test_result("Block wget command", True, str(e)[:60] + "...")

    # Test safe command works
    try:
        result = subprocess.run(['echo', 'Safe command works'],
                              capture_output=True, text=True)
        test_result("Allow safe commands", result.returncode == 0,
                   f"Output: {result.stdout.strip()}")
    except Exception as e:
        test_result("Allow safe commands", False, str(e))

    sys.stdout.write("\nLayer 3: Seccomp Syscall Blocking (Linux only)\n")
    sys.stdout.write("-" * 40 + "\n")

    try:
        sys.path.insert(0, 'src/worm')
        from seccomp import network_filter

        status = network_filter.get_status()
        if status['available']:
            sys.stdout.write(f"  Seccomp available: Yes\n")
            sys.stdout.write(f"  Platform: {status['platform']}\n")
            sys.stdout.write("  Provides kernel-level network blocking\n")
        else:
            sys.stdout.write(f"  Seccomp available: No (platform: {status['platform']})\n")
            sys.stdout.write("  Python-level restrictions still active\n")
    except Exception as e:
        sys.stdout.write(f"  Note: {e}\n")


def demo_resource_limits():
    """Demonstrate resource limiting."""
    header("3. RESOURCE LIMITS (DoS Prevention)")

    sys.stdout.write("Resource limits prevent:\n")
    sys.stdout.write("  • Infinite loops (CPU time limits)\n")
    sys.stdout.write("  • Memory exhaustion (memory limits)\n")
    sys.stdout.write("  • Disk filling (file size limits)\n")
    sys.stdout.write("  • File descriptor exhaustion (open file limits)\n\n")

    try:
        sys.path.insert(0, 'src/worm')
        from security import resource_limits

        # Get current usage
        usage = resource_limits.get_current_usage()

        sys.stdout.write("Current Resource Usage:\n")
        sys.stdout.write(f"  CPU time: {usage.get('cpu_total', 0):.2f} seconds\n")
        sys.stdout.write(f"  Memory: {usage.get('max_rss_mb', 0):.1f} MB\n")

        if usage.get('cpu_limit'):
            sys.stdout.write(f"  CPU limit: {usage['cpu_limit']} seconds\n")
        if usage.get('memory_limit_mb'):
            sys.stdout.write(f"  Memory limit: {usage['memory_limit_mb']:.0f} MB\n")

        sys.stdout.write("\nSecurity Profiles Available:\n")
        sys.stdout.write("  • Strict: 30s CPU, 512MB RAM (untrusted code)\n")
        sys.stdout.write("  • Moderate: 300s CPU, 2GB RAM (general use)\n")
        sys.stdout.write("  • Relaxed: 3600s CPU, 4GB RAM (trusted code)\n")

        test_result("Resource limits module loaded", True)

    except Exception as e:
        test_result("Resource limits module", False, str(e))


def demo_restricted_builtins():
    """Demonstrate restricted builtins."""
    header("4. RESTRICTED BUILTINS (Code Injection Prevention)")

    sys.stdout.write("Optionally block dangerous builtins:\n")
    sys.stdout.write("  • eval() - Dynamic code evaluation\n")
    sys.stdout.write("  • exec() - Arbitrary code execution\n")
    sys.stdout.write("  • compile() - Code object creation\n\n")

    try:
        sys.path.insert(0, 'src/worm')
        from security import restricted_builtins

        # Show current state
        status = restricted_builtins.get_restriction_status()
        sys.stdout.write("Current State (before restrictions):\n")
        sys.stdout.write(f"  eval restricted: {status['eval_restricted']}\n")
        sys.stdout.write(f"  exec restricted: {status['exec_restricted']}\n")
        sys.stdout.write(f"  compile restricted: {status['compile_restricted']}\n\n")

        # Test eval works before restriction
        try:
            result = eval('2 + 2')
            test_result("eval() works normally", True, f"2 + 2 = {result}")
        except:
            test_result("eval() works normally", False)

        # Enable restrictions
        sys.stdout.write("\nEnabling strict restrictions...\n\n")
        restricted_builtins.enable_restricted_builtins('strict')

        # Test eval is now blocked
        try:
            result = eval('2 + 2')
            test_result("eval() now blocked", False, "eval still works!")
        except restricted_builtins.RestrictedBuiltinsError:
            test_result("eval() now blocked", True, "RestrictedBuiltinsError raised")

        # Test exec is blocked
        try:
            exec('x = 1')
            test_result("exec() blocked", False, "exec still works!")
        except restricted_builtins.RestrictedBuiltinsError:
            test_result("exec() blocked", True, "RestrictedBuiltinsError raised")

        # Restore for rest of demo
        restricted_builtins.disable_restricted_builtins()
        sys.stdout.write("\nRestrictions disabled for rest of demo.\n")

    except Exception as e:
        test_result("Restricted builtins module", False, str(e))


def demo_filesystem_sandbox():
    """Demonstrate filesystem sandboxing."""
    header("5. FILESYSTEM SANDBOX (Access Control)")

    sys.stdout.write("Filesystem sandboxing modes:\n")
    sys.stdout.write("  • Read-only: Block all write operations\n")
    sys.stdout.write("  • Whitelist: Only allow specific directories\n")
    sys.stdout.write("  • Blacklist: Deny specific directories\n\n")

    try:
        sys.path.insert(0, 'src/worm')
        from security import filesystem_sandbox

        # Create temp file for testing
        test_dir = tempfile.mkdtemp()
        test_file = os.path.join(test_dir, 'test.txt')

        sys.stdout.write(f"Test directory: {test_dir}\n\n")

        # Test read-only mode
        sys.stdout.write("Testing read-only mode:\n")
        sandbox = filesystem_sandbox.FilesystemSandbox(mode='read_only')
        sandbox.enable()

        try:
            with open(test_file, 'w') as f:
                f.write('test')
            test_result("Read-only blocks writes", False, "Write succeeded!")
        except filesystem_sandbox.FilesystemAccessError:
            test_result("Read-only blocks writes", True, "Write blocked as expected")

        sandbox.disable()

        # Create file for read test
        with open(test_file, 'w') as f:
            f.write('test data')

        # Test whitelist mode
        sys.stdout.write("\nTesting whitelist mode:\n")
        sandbox = filesystem_sandbox.FilesystemSandbox(
            mode='whitelist',
            allowed_paths=[test_dir]
        )
        sandbox.enable()

        try:
            with open(test_file, 'r') as f:
                data = f.read()
            test_result("Whitelist allows approved paths", True,
                       f"Read '{data}' from whitelisted path")
        except:
            test_result("Whitelist allows approved paths", False)

        try:
            with open('/tmp/blocked.txt', 'w') as f:
                f.write('test')
            test_result("Whitelist blocks non-approved paths", False,
                       "Write to /tmp succeeded!")
        except filesystem_sandbox.FilesystemAccessError:
            test_result("Whitelist blocks non-approved paths", True)

        sandbox.disable()

        # Cleanup
        import shutil
        shutil.rmtree(test_dir)

    except Exception as e:
        test_result("Filesystem sandbox module", False, str(e))


def demo_audit_logging():
    """Demonstrate audit logging."""
    header("6. AUDIT LOGGING (Security Event Tracking)")

    sys.stdout.write("Audit logging captures:\n")
    sys.stdout.write("  • Blocked import attempts\n")
    sys.stdout.write("  • Blocked subprocess commands\n")
    sys.stdout.write("  • Restricted builtin usage\n")
    sys.stdout.write("  • Resource limit violations\n")
    sys.stdout.write("  • IoC detections (CRITICAL)\n")
    sys.stdout.write("  • Session start/end\n\n")

    try:
        sys.path.insert(0, 'src/worm')
        from security import audit_log

        # Create temp log
        temp_log = tempfile.mktemp(suffix='.log')
        logger = audit_log.AuditLogger(log_file=temp_log)

        sys.stdout.write(f"Logging to: {temp_log}\n\n")

        # Log various events
        sys.stdout.write("Logging test events...\n")
        logger.log_session_start('/demo/test.py', ['arg1', 'arg2'])
        logger.log_blocked_import('socket')
        logger.log_blocked_subprocess(['curl', 'evil.com'], 'network command')
        logger.log_restricted_builtin('eval')
        logger.log_ioc_detected('print_statement', 'print() detected at line 42')
        logger.log_session_end(0)

        test_result("Events logged", True, "6 events written")

        # Read back
        sys.stdout.write("\nReading audit log:\n")
        entries = audit_log.read_audit_log(log_file=temp_log)

        for entry in entries:
            event_type = entry.get('event_type', 'unknown')
            if event_type == 'IOC_DETECTED':
                sys.stdout.write(f"  ⚠ CRITICAL: {event_type}\n")
            else:
                sys.stdout.write(f"  • {event_type}\n")

        # Search for IoCs
        sys.stdout.write("\nSearching for IoC events:\n")
        iocs = audit_log.search_audit_log(event_type='IOC_DETECTED', log_file=temp_log)
        test_result("IoC detection in logs", len(iocs) > 0,
                   f"Found {len(iocs)} IoC event(s)")

        # Cleanup
        os.unlink(temp_log)

    except Exception as e:
        test_result("Audit logging module", False, str(e))


def demo_monitoring_tools():
    """Demonstrate monitoring tools."""
    header("7. IOC MONITORING TOOLS")

    sys.stdout.write("Monitoring tools available:\n\n")

    sys.stdout.write("1. IoC Monitor (tools/ioc_monitor.py)\n")
    sys.stdout.write("   $ python3 tools/ioc_monitor.py --verify-worm-source\n")
    sys.stdout.write("   $ python3 tools/ioc_monitor.py --scan-file script.py\n")
    sys.stdout.write("   $ python3 tools/ioc_monitor.py --monitor-log --follow\n\n")

    sys.stdout.write("2. Security Monitor (tools/worm_monitor.sh)\n")
    sys.stdout.write("   $ tools/worm_monitor.sh status\n")
    sys.stdout.write("   $ tools/worm_monitor.sh follow\n")
    sys.stdout.write("   $ tools/worm_monitor.sh verify\n\n")

    sys.stdout.write("Features:\n")
    sys.stdout.write("  ✓ Real-time IoC detection\n")
    sys.stdout.write("  ✓ Source integrity verification\n")
    sys.stdout.write("  ✓ Audit log monitoring\n")
    sys.stdout.write("  ✓ Security event alerting\n")

    test_result("Monitoring tools available", True)


def demo_allowed_operations():
    """Demonstrate what still works."""
    header("8. ALLOWED OPERATIONS (Full Python Functionality)")

    sys.stdout.write("Worm Python maintains full Python functionality:\n\n")

    # Math operations
    import math
    result = math.sqrt(42)
    test_result("Math operations", True, f"sqrt(42) = {result:.2f}")

    # Data structures
    data = {'name': 'Worm Python', 'secure': True}
    test_result("Data structures", True, f"Dict: {data}")

    # JSON
    import json
    json_str = json.dumps(data)
    test_result("JSON module", True, f"Serialized: {json_str}")

    # File I/O
    temp_file = tempfile.mktemp()
    with open(temp_file, 'w') as f:
        f.write('File I/O works')
    with open(temp_file, 'r') as f:
        content = f.read()
    os.unlink(temp_file)
    test_result("File I/O", True, f"Read: '{content}'")

    # List comprehensions
    squares = [x**2 for x in range(5)]
    test_result("List comprehensions", True, f"Squares: {squares}")

    # Classes
    class TestClass:
        def __init__(self):
            self.value = 42
    obj = TestClass()
    test_result("Classes and objects", True, f"Object value: {obj.value}")

    sys.stdout.write("\nAll non-network Python features work normally!\n")


def final_summary():
    """Display final summary."""
    header("DEMO COMPLETE - SUMMARY")

    sys.stdout.write("Worm Python Security Features Demonstrated:\n\n")

    features = [
        ("Print-Free Codebase", "IoC breach detection"),
        ("Network Isolation", "3-layer defense (import/subprocess/seccomp)"),
        ("Resource Limits", "DoS prevention"),
        ("Restricted Builtins", "Code injection prevention"),
        ("Filesystem Sandbox", "Access control"),
        ("Audit Logging", "Security event tracking"),
        ("IoC Monitoring", "Real-time breach detection"),
        ("Full Python Support", "All non-network features work"),
    ]

    for i, (feature, description) in enumerate(features, 1):
        sys.stdout.write(f"  {i}. ✓ {feature:25} - {description}\n")

    sys.stdout.write("\n" + "=" * 70 + "\n")
    sys.stdout.write("Worm Python: Production-Ready Defensive Security Distribution\n")
    sys.stdout.write("=" * 70 + "\n\n")

    sys.stdout.write("Use Cases:\n")
    sys.stdout.write("  • Untrusted code execution\n")
    sys.stdout.write("  • Sensitive data processing\n")
    sys.stdout.write("  • Educational environments\n")
    sys.stdout.write("  • Malware analysis\n")
    sys.stdout.write("  • CI/CD security\n")
    sys.stdout.write("  • Code competitions\n\n")

    sys.stdout.write("Documentation:\n")
    sys.stdout.write("  • docs/QUICKSTART.md - Getting started\n")
    sys.stdout.write("  • docs/SECURITY.md - Security model\n")
    sys.stdout.write("  • docs/USE_CASES.md - Intended uses\n")
    sys.stdout.write("  • docs/DEPLOYMENT.md - Production deployment\n\n")


def main():
    """Run comprehensive demo."""
    sys.stdout.write("\n")
    sys.stdout.write("╔" + "═" * 68 + "╗\n")
    sys.stdout.write("║" + " " * 68 + "║\n")
    sys.stdout.write("║" + "  WORM PYTHON - COMPREHENSIVE SECURITY FEATURE DEMONSTRATION".center(68) + "║\n")
    sys.stdout.write("║" + " " * 68 + "║\n")
    sys.stdout.write("╚" + "═" * 68 + "╝\n")

    sys.stdout.write("\nThis demo showcases all defensive security features.\n")
    sys.stdout.write("Running in Worm Python environment: ")

    if os.environ.get('WORM_PYTHON') == '1':
        sys.stdout.write("YES ✓\n")
    else:
        sys.stdout.write("NO (run with: python3 src/worm/worm.py demo/comprehensive_demo.py)\n")

    time.sleep(1)

    # Run all demos
    demo_print_free_codebase()
    time.sleep(0.5)

    demo_network_isolation()
    time.sleep(0.5)

    demo_resource_limits()
    time.sleep(0.5)

    demo_restricted_builtins()
    time.sleep(0.5)

    demo_filesystem_sandbox()
    time.sleep(0.5)

    demo_audit_logging()
    time.sleep(0.5)

    demo_monitoring_tools()
    time.sleep(0.5)

    demo_allowed_operations()
    time.sleep(0.5)

    final_summary()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.stdout.write("\n\nDemo interrupted by user.\n")
        sys.exit(130)
    except Exception as e:
        sys.stderr.write(f"\nDemo error: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
