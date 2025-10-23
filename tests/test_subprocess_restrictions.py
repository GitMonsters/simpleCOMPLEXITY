"""
Tests for subprocess restriction functionality
"""

import sys
import pytest


def test_restricted_subprocess_module():
    """Test that restricted_subprocess module loads correctly."""
    sys.path.insert(0, 'src/worm')
    from modules.restricted_subprocess import NetworkCommandError
    assert issubclass(NetworkCommandError, Exception)


def test_curl_blocked():
    """Test that curl command is blocked."""
    sys.path.insert(0, 'src/worm')
    from modules import restricted_subprocess

    with pytest.raises(restricted_subprocess.NetworkCommandError):
        restricted_subprocess.run(['curl', 'example.com'])


def test_wget_blocked():
    """Test that wget command is blocked."""
    sys.path.insert(0, 'src/worm')
    from modules import restricted_subprocess

    with pytest.raises(restricted_subprocess.NetworkCommandError):
        restricted_subprocess.run(['wget', 'http://example.com'])


def test_ping_blocked():
    """Test that ping command is blocked."""
    sys.path.insert(0, 'src/worm')
    from modules import restricted_subprocess

    with pytest.raises(restricted_subprocess.NetworkCommandError):
        restricted_subprocess.run(['ping', 'example.com'])


def test_ssh_blocked():
    """Test that ssh command is blocked."""
    sys.path.insert(0, 'src/worm')
    from modules import restricted_subprocess

    with pytest.raises(restricted_subprocess.NetworkCommandError):
        restricted_subprocess.run(['ssh', 'user@host'])


def test_nc_blocked():
    """Test that netcat command is blocked."""
    sys.path.insert(0, 'src/worm')
    from modules import restricted_subprocess

    with pytest.raises(restricted_subprocess.NetworkCommandError):
        restricted_subprocess.run(['nc', 'example.com', '80'])


def test_url_pattern_blocked():
    """Test that commands with URL patterns are blocked."""
    sys.path.insert(0, 'src/worm')
    from modules import restricted_subprocess

    with pytest.raises(restricted_subprocess.NetworkCommandError):
        restricted_subprocess.run(['python3', '-c', 'import urllib; urllib.request.urlopen("http://example.com")'])


def test_safe_commands_allowed():
    """Test that safe commands are allowed."""
    sys.path.insert(0, 'src/worm')
    from modules import restricted_subprocess

    # These should all work
    result = restricted_subprocess.run(['echo', 'hello'], capture_output=True, text=True)
    assert result.returncode == 0
    assert 'hello' in result.stdout

    result = restricted_subprocess.run(['ls', '-la'], capture_output=True)
    assert result.returncode == 0

    result = restricted_subprocess.run(['python3', '--version'], capture_output=True, text=True)
    assert result.returncode == 0


def test_subprocess_constants_available():
    """Test that subprocess constants are available."""
    sys.path.insert(0, 'src/worm')
    from modules import restricted_subprocess

    assert hasattr(restricted_subprocess, 'PIPE')
    assert hasattr(restricted_subprocess, 'STDOUT')
    assert hasattr(restricted_subprocess, 'DEVNULL')
    assert hasattr(restricted_subprocess, 'CalledProcessError')
    assert hasattr(restricted_subprocess, 'TimeoutExpired')


def test_popen_blocked_for_network():
    """Test that Popen is blocked for network commands."""
    sys.path.insert(0, 'src/worm')
    from modules import restricted_subprocess

    with pytest.raises(restricted_subprocess.NetworkCommandError):
        restricted_subprocess.Popen(['curl', 'example.com'])


def test_popen_allowed_for_safe():
    """Test that Popen works for safe commands."""
    sys.path.insert(0, 'src/worm')
    from modules import restricted_subprocess

    proc = restricted_subprocess.Popen(['echo', 'test'], stdout=restricted_subprocess.PIPE)
    output, _ = proc.communicate()
    assert proc.returncode == 0
    assert b'test' in output


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
