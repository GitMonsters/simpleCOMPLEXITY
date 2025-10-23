#!/usr/bin/env python3
"""
ATTACK SIMULATION: Resource Exhaustion (DoS)

This script simulates DoS attacks via resource exhaustion.
When run in Worm Python with resource limits, attacks are prevented.

DEFENSIVE USE ONLY: This demonstrates what Worm Python prevents.
"""

import sys
import time


def attempt_infinite_loop():
    """Attempt to hang system with infinite loop."""
    sys.stdout.write("ATTACK: Attempting infinite loop (CPU exhaustion)...\n")

    try:
        sys.stdout.write("  Starting infinite loop...\n")
        sys.stdout.write("  (Will be killed by CPU time limit if enabled)\n")

        start = time.time()
        count = 0

        while True:
            count += 1
            if count % 10000000 == 0:
                elapsed = time.time() - start
                sys.stdout.write(f"    Loop running: {elapsed:.1f}s, {count:,} iterations\n")

                # Exit after 5 seconds for demo purposes
                if elapsed > 5:
                    sys.stdout.write("  ✗ VULNERABLE: Infinite loop not stopped\n")
                    sys.stdout.write("    (Run with CPU limits to prevent this)\n")
                    return False

    except Exception as e:
        # Killed by resource limit
        sys.stdout.write(f"  ✓ BLOCKED: {type(e).__name__}\n")
        sys.stdout.write("    CPU time limit enforced\n")
        return True


def attempt_memory_exhaustion():
    """Attempt to exhaust system memory."""
    sys.stdout.write("\nATTACK: Attempting memory exhaustion...\n")

    try:
        sys.stdout.write("  Allocating large amounts of memory...\n")

        huge_list = []
        mb_allocated = 0

        for i in range(1000):
            # Allocate 1MB chunks
            huge_list.append([0] * (1024 * 256))  # ~1MB
            mb_allocated += 1

            if mb_allocated % 100 == 0:
                sys.stdout.write(f"    Allocated: {mb_allocated} MB\n")

                # Stop at 500MB for demo
                if mb_allocated >= 500:
                    sys.stdout.write("  ✗ VULNERABLE: Memory exhaustion not prevented\n")
                    sys.stdout.write("    (Run with memory limits to prevent this)\n")
                    return False

    except MemoryError:
        sys.stdout.write(f"  ✓ BLOCKED: MemoryError - limit enforced\n")
        sys.stdout.write(f"    Stopped at ~{mb_allocated} MB\n")
        return True


def attempt_file_bomb():
    """Attempt to fill disk with large file."""
    sys.stdout.write("\nATTACK: Attempting disk space exhaustion...\n")

    import tempfile
    import os

    try:
        temp_file = tempfile.mktemp()
        sys.stdout.write(f"  Creating large file: {temp_file}\n")

        with open(temp_file, 'wb') as f:
            mb_written = 0

            for i in range(100):
                # Write 1MB chunks
                f.write(b'0' * (1024 * 1024))
                mb_written += 1

                if mb_written % 10 == 0:
                    sys.stdout.write(f"    Written: {mb_written} MB\n")

                # Stop at 50MB for demo
                if mb_written >= 50:
                    sys.stdout.write("  ✗ VULNERABLE: File size not limited\n")
                    sys.stdout.write("    (Run with file size limits to prevent this)\n")
                    os.unlink(temp_file)
                    return False

    except OSError as e:
        sys.stdout.write(f"  ✓ BLOCKED: {type(e).__name__}\n")
        sys.stdout.write("    File size limit enforced\n")
        try:
            os.unlink(temp_file)
        except:
            pass
        return True


def attempt_file_descriptor_exhaustion():
    """Attempt to exhaust file descriptors."""
    sys.stdout.write("\nATTACK: Attempting file descriptor exhaustion...\n")

    import tempfile

    try:
        sys.stdout.write("  Opening many files simultaneously...\n")

        files = []
        for i in range(10000):
            try:
                f = tempfile.TemporaryFile()
                files.append(f)

                if len(files) % 100 == 0:
                    sys.stdout.write(f"    Open files: {len(files)}\n")

            except OSError:
                sys.stdout.write(f"  ✓ BLOCKED: OSError after {len(files)} files\n")
                sys.stdout.write("    File descriptor limit enforced\n")

                # Clean up
                for f in files:
                    f.close()

                return True

        sys.stdout.write(f"  ✗ VULNERABLE: Opened {len(files)} files without limit\n")
        sys.stdout.write("    (Run with open file limits to prevent this)\n")

        # Clean up
        for f in files:
            f.close()

        return False

    except Exception as e:
        sys.stdout.write(f"  Unexpected error: {e}\n")
        return False


def main():
    sys.stdout.write("=" * 70 + "\n")
    sys.stdout.write("ATTACK SIMULATION: Resource Exhaustion (DoS)\n")
    sys.stdout.write("=" * 70 + "\n\n")

    sys.stdout.write("Simulating resource exhaustion attacks...\n")
    sys.stdout.write("Run with Worm Python resource limits to block these.\n\n")

    sys.stdout.write("NOTE: These simulations are limited for demo purposes.\n")
    sys.stdout.write("      Real attacks would be more severe.\n\n")

    results = []

    # Note: Infinite loop test is aggressive, skip by default
    sys.stdout.write("SKIPPING: Infinite loop test (too aggressive for demo)\n")
    sys.stdout.write("  To enable: Run with --cpu-limit flag\n\n")

    results.append(attempt_memory_exhaustion())
    results.append(attempt_file_bomb())
    results.append(attempt_file_descriptor_exhaustion())

    sys.stdout.write("\n" + "=" * 70 + "\n")
    sys.stdout.write(f"RESULT: {sum(results)}/{len(results)} attacks blocked\n")

    if all(results):
        sys.stdout.write("✓ PROTECTED: Resource limits enforced\n")
    else:
        sys.stdout.write("⚠ WARNING: Run with resource limits enabled\n")
        sys.stdout.write("  Example: worm --moderate resource_exhaustion.py\n")

    sys.stdout.write("=" * 70 + "\n")


if __name__ == '__main__':
    main()
