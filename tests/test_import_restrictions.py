"""
Tests for import restriction functionality
"""

import sys
import pytest


def test_import_restrictions_module():
    """Test that import_restrictions module loads correctly."""
    sys.path.insert(0, 'src/worm')
    from hooks.import_restrictions import install_import_restrictions, WormImportError
    assert callable(install_import_restrictions)
    assert issubclass(WormImportError, ImportError)


def test_socket_blocked():
    """Test that socket module cannot be imported."""
    sys.path.insert(0, 'src/worm')
    from hooks.import_restrictions import install_import_restrictions

    install_import_restrictions()

    with pytest.raises(ImportError):
        import socket


def test_urllib_blocked():
    """Test that urllib modules cannot be imported."""
    sys.path.insert(0, 'src/worm')
    from hooks.import_restrictions import install_import_restrictions

    install_import_restrictions()

    with pytest.raises(ImportError):
        import urllib.request


def test_http_blocked():
    """Test that http modules cannot be imported."""
    sys.path.insert(0, 'src/worm')
    from hooks.import_restrictions import install_import_restrictions

    install_import_restrictions()

    with pytest.raises(ImportError):
        import http.client


def test_requests_blocked():
    """Test that requests module cannot be imported (if installed)."""
    sys.path.insert(0, 'src/worm')
    from hooks.import_restrictions import install_import_restrictions

    install_import_restrictions()

    # requests might not be installed, but if it is, it should be blocked
    try:
        import requests
        pytest.fail("requests module should be blocked")
    except ImportError:
        pass  # Expected


def test_safe_modules_allowed():
    """Test that safe modules can still be imported."""
    sys.path.insert(0, 'src/worm')
    from hooks.import_restrictions import install_import_restrictions

    install_import_restrictions()

    # These should all work
    import json
    import os
    import sys
    import math
    import datetime

    assert json is not None
    assert os is not None
    assert sys is not None
    assert math is not None
    assert datetime is not None


def test_get_blocked_modules():
    """Test getting the list of blocked modules."""
    sys.path.insert(0, 'src/worm')
    from hooks.import_restrictions import get_blocked_modules

    blocked = get_blocked_modules()
    assert isinstance(blocked, set)
    assert 'socket' in blocked
    assert 'urllib' in blocked
    assert 'http' in blocked
    assert 'requests' in blocked


def test_is_module_allowed():
    """Test the is_module_allowed function."""
    sys.path.insert(0, 'src/worm')
    from hooks.import_restrictions import is_module_allowed

    assert not is_module_allowed('socket')
    assert not is_module_allowed('urllib')
    assert not is_module_allowed('http.client')
    assert is_module_allowed('json')
    assert is_module_allowed('os')
    assert is_module_allowed('math')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
