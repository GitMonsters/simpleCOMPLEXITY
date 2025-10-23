#!/usr/bin/env python3
"""
Worm Python Performance Benchmark

Measures the performance overhead of security features.
Compares standard Python vs Worm Python execution.
"""

import sys
import time
import subprocess
import tempfile
import os


def benchmark_test(name, code, iterations=100):
    """Run a benchmark test."""
    sys.stdout.write(f"\nBenchmarking: {name}\n")
    sys.stdout.write("-" * 60 + "\n")

    # Create temp file with code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_file = f.name

    try:
        # Benchmark standard Python
        start = time.time()
        for _ in range(iterations):
            subprocess.run(
                ['python3', temp_file],
                capture_output=True,
                timeout=5
            )
        python_time = time.time() - start

        # Benchmark Worm Python
        start = time.time()
        for _ in range(iterations):
            subprocess.run(
                ['python3', 'src/worm/worm.py', temp_file],
                capture_output=True,
                timeout=5
            )
        worm_time = time.time() - start

        # Calculate overhead
        overhead_ms = ((worm_time - python_time) / iterations) * 1000
        overhead_pct = ((worm_time / python_time) - 1) * 100

        sys.stdout.write(f"Standard Python: {python_time:.3f}s ({iterations} runs)\n")
        sys.stdout.write(f"Worm Python:     {worm_time:.3f}s ({iterations} runs)\n")
        sys.stdout.write(f"Per-run overhead: {overhead_ms:.2f}ms ({overhead_pct:+.1f}%)\n")

        return {
            'name': name,
            'python_time': python_time,
            'worm_time': worm_time,
            'overhead_ms': overhead_ms,
            'overhead_pct': overhead_pct,
        }

    finally:
        os.unlink(temp_file)


def main():
    sys.stdout.write("=" * 70 + "\n")
    sys.stdout.write("Worm Python Performance Benchmark\n")
    sys.stdout.write("=" * 70 + "\n")
    sys.stdout.write("\nMeasuring security overhead across different workloads...\n")

    results = []

    # Test 1: Minimal program
    results.append(benchmark_test(
        "Minimal Program",
        "import sys\nsys.stdout.write('test\\n')",
        iterations=100
    ))

    # Test 2: Math-heavy
    results.append(benchmark_test(
        "Math Operations",
        """
import math
result = sum(math.sqrt(i) for i in range(1000))
        """,
        iterations=50
    ))

    # Test 3: File I/O
    results.append(benchmark_test(
        "File I/O",
        """
import tempfile
import os
f = tempfile.mktemp()
with open(f, 'w') as fp:
    fp.write('test' * 1000)
with open(f, 'r') as fp:
    data = fp.read()
os.unlink(f)
        """,
        iterations=50
    ))

    # Test 4: JSON operations
    results.append(benchmark_test(
        "JSON Serialization",
        """
import json
data = {'key': 'value', 'numbers': list(range(100))}
for _ in range(100):
    json.dumps(data)
    json.loads('{"test": 123}')
        """,
        iterations=50
    ))

    # Summary
    sys.stdout.write("\n" + "=" * 70 + "\n")
    sys.stdout.write("BENCHMARK SUMMARY\n")
    sys.stdout.write("=" * 70 + "\n\n")

    sys.stdout.write(f"{'Test':<25} {'Overhead (ms)':<15} {'Overhead (%)':<15}\n")
    sys.stdout.write("-" * 70 + "\n")

    for r in results:
        sys.stdout.write(f"{r['name']:<25} {r['overhead_ms']:>10.2f} ms   {r['overhead_pct']:>10.1f}%\n")

    avg_overhead = sum(r['overhead_ms'] for r in results) / len(results)
    sys.stdout.write("-" * 70 + "\n")
    sys.stdout.write(f"{'Average':<25} {avg_overhead:>10.2f} ms\n")

    sys.stdout.write("\n" + "=" * 70 + "\n")
    sys.stdout.write("ANALYSIS\n")
    sys.stdout.write("=" * 70 + "\n\n")

    sys.stdout.write("The overhead is primarily from:\n")
    sys.stdout.write("  1. Import hook installation (one-time startup cost)\n")
    sys.stdout.write("  2. Module replacement (subprocess, etc.)\n")
    sys.stdout.write("  3. Security initialization\n\n")

    sys.stdout.write("For long-running programs, the overhead is negligible.\n")
    sys.stdout.write("Security benefits far outweigh minimal performance cost.\n\n")

    if avg_overhead < 50:
        sys.stdout.write("✓ Excellent: Overhead < 50ms\n")
    elif avg_overhead < 100:
        sys.stdout.write("✓ Good: Overhead < 100ms\n")
    else:
        sys.stdout.write("⚠ Note: Higher overhead detected\n")


if __name__ == '__main__':
    # Check if worm.py exists
    if not os.path.exists('src/worm/worm.py'):
        sys.stderr.write("Error: Run this from the COMPLEXITY directory\n")
        sys.exit(1)

    main()
