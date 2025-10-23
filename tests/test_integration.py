"""
Integration tests for Worm Python

These tests run actual worm Python scripts to verify end-to-end functionality.
"""

import subprocess
import sys
import os
import pytest


# Path to worm.py
WORM_PY = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src', 'worm', 'worm.py')


def run_worm(code):
    """
    Run code using worm Python and return the result.

    Args:
        code: Python code to execute

    Returns:
        subprocess.CompletedProcess object
    """
    result = subprocess.run(
        [sys.executable, WORM_PY, '-c', code],
        capture_output=True,
        text=True,
        timeout=5
    )
    return result


def test_worm_help():
    """Test that worm --help works."""
    result = subprocess.run(
        [sys.executable, WORM_PY, '--help'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert 'Worm Python' in result.stdout
    assert 'Security' in result.stdout


def test_worm_version():
    """Test that worm --version works."""
    result = subprocess.run(
        [sys.executable, WORM_PY, '--version'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert 'Worm Python' in result.stdout
    assert '0.1.0' in result.stdout


def test_worm_info():
    """Test that worm --info works."""
    result = subprocess.run(
        [sys.executable, WORM_PY, '--info'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert 'Worm Python' in result.stdout
    assert 'Security Features' in result.stdout


def test_print_works():
    """Test that basic print functionality works."""
    result = run_worm('print("Hello from Worm Python")')
    assert result.returncode == 0
    assert 'Hello from Worm Python' in result.stdout


def test_math_works():
    """Test that mathematical operations work."""
    result = run_worm('import math; print(math.pi)')
    assert result.returncode == 0
    assert '3.14' in result.stdout


def test_json_works():
    """Test that JSON module works."""
    result = run_worm('import json; print(json.dumps({"test": "ok"}))')
    assert result.returncode == 0
    assert '"test"' in result.stdout
    assert '"ok"' in result.stdout


def test_socket_blocked():
    """Test that socket import is blocked."""
    result = run_worm('import socket')
    assert result.returncode != 0
    assert 'disabled' in result.stderr.lower() or 'blocked' in result.stderr.lower()


def test_urllib_blocked():
    """Test that urllib import is blocked."""
    result = run_worm('import urllib.request')
    assert result.returncode != 0
    assert 'disabled' in result.stderr.lower() or 'blocked' in result.stderr.lower()


def test_http_blocked():
    """Test that http import is blocked."""
    result = run_worm('import http.client')
    assert result.returncode != 0
    assert 'disabled' in result.stderr.lower() or 'blocked' in result.stderr.lower()


def test_subprocess_safe_command():
    """Test that subprocess with safe commands works."""
    result = run_worm('import subprocess; r = subprocess.run(["echo", "test"], capture_output=True); print(r.stdout)')
    assert result.returncode == 0


def test_subprocess_curl_blocked():
    """Test that subprocess curl is blocked."""
    result = run_worm('import subprocess; subprocess.run(["curl", "example.com"])')
    assert result.returncode != 0
    assert 'blocked' in result.stderr.lower() or 'network' in result.stderr.lower()


def test_file_operations_work():
    """Test that file I/O operations work."""
    code = '''
import tempfile
import os
with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
    f.write("test data")
    fname = f.name
with open(fname, 'r') as f:
    data = f.read()
print(data)
os.unlink(fname)
'''
    result = run_worm(code)
    assert result.returncode == 0
    assert 'test data' in result.stdout


def test_list_comprehension():
    """Test that Python comprehensions work."""
    result = run_worm('print([x*2 for x in range(5)])')
    assert result.returncode == 0
    assert '[0, 2, 4, 6, 8]' in result.stdout


def test_classes_work():
    """Test that Python classes work."""
    code = '''
class TestClass:
    def __init__(self, value):
        self.value = value
    def get_value(self):
        return self.value * 2

obj = TestClass(21)
print(obj.get_value())
'''
    result = run_worm(code)
    assert result.returncode == 0
    assert '42' in result.stdout


def test_exception_handling():
    """Test that exception handling works."""
    code = '''
try:
    x = 1 / 0
except ZeroDivisionError:
    print("Caught division by zero")
'''
    result = run_worm(code)
    assert result.returncode == 0
    assert 'Caught division by zero' in result.stdout


def test_worm_environment_variable():
    """Test that WORM_PYTHON environment variable is set."""
    code = 'import os; print(os.environ.get("WORM_PYTHON", "not set"))'
    result = run_worm(code)
    assert result.returncode == 0
    assert '1' in result.stdout


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
