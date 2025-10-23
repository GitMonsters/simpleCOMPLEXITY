"""
Worm Python Import Hook System

This module implements import restrictions to prevent loading of
network-capable modules and other potentially dangerous functionality.
"""

import sys
import importlib.abc
import importlib.machinery


# Modules that are completely blocked
BLOCKED_MODULES = {
    'socket',
    'socketserver',
    'http',
    'http.client',
    'http.server',
    'urllib',
    'urllib.request',
    'urllib.parse',
    'urllib3',
    'requests',
    'aiohttp',
    'httpx',
    'ftplib',
    'poplib',
    'imaplib',
    'smtplib',
    'telnetlib',
    'xmlrpc',
    'xmlrpc.client',
    'xmlrpc.server',
}

# Modules that require restricted versions
RESTRICTED_MODULES = {
    'subprocess',  # Block network commands
    'os',          # Restrict certain operations
}


class WormImportError(ImportError):
    """Custom exception for blocked imports in Worm Python."""
    pass


class NetworkModuleBlocker(importlib.abc.MetaPathFinder):
    """
    Meta path finder that blocks network-related module imports.

    This is the first line of defense against network access,
    preventing dangerous modules from being loaded at all.
    """

    def find_spec(self, fullname, path, target=None):
        """Check if module should be blocked."""
        # Check direct module name
        if fullname in BLOCKED_MODULES:
            raise WormImportError(
                f"Module '{fullname}' is disabled in Worm Python for security reasons. "
                f"This distribution blocks all network-capable modules. "
                f"If you need network access, use standard Python instead."
            )

        # Check if it's a submodule of a blocked module
        for blocked in BLOCKED_MODULES:
            if fullname.startswith(blocked + '.'):
                raise WormImportError(
                    f"Module '{fullname}' is disabled in Worm Python for security reasons. "
                    f"This distribution blocks all network-capable modules. "
                    f"If you need network access, use standard Python instead."
                )

        # Not a blocked module, let normal import proceed
        return None

    def find_module(self, fullname, path=None):
        """Legacy find_module for Python 3.4+ compatibility."""
        if fullname in BLOCKED_MODULES:
            return self

        for blocked in BLOCKED_MODULES:
            if fullname.startswith(blocked + '.'):
                return self

        return None

    def load_module(self, fullname):
        """Raise error when trying to load a blocked module."""
        raise WormImportError(
            f"Module '{fullname}' is disabled in Worm Python for security reasons. "
            f"This distribution blocks all network-capable modules. "
            f"If you need network access, use standard Python instead."
        )


def install_import_restrictions():
    """
    Install the import hook system.

    This should be called as early as possible in the Python startup process.
    """
    # Install our custom meta path finder at the beginning
    blocker = NetworkModuleBlocker()
    sys.meta_path.insert(0, blocker)

    # Remove already-imported network modules if any
    modules_to_remove = []
    for module_name in sys.modules:
        if module_name in BLOCKED_MODULES:
            modules_to_remove.append(module_name)
        else:
            for blocked in BLOCKED_MODULES:
                if module_name.startswith(blocked + '.'):
                    modules_to_remove.append(module_name)
                    break

    for module_name in modules_to_remove:
        del sys.modules[module_name]

    return blocker


def is_module_allowed(module_name):
    """Check if a module is allowed to be imported."""
    if module_name in BLOCKED_MODULES:
        return False

    for blocked in BLOCKED_MODULES:
        if module_name.startswith(blocked + '.'):
            return False

    return True


def get_blocked_modules():
    """Return the set of blocked module names."""
    return BLOCKED_MODULES.copy()


if __name__ == '__main__':
    # Test the import restrictions
    install_import_restrictions()

    sys.stdout.write("Testing Worm Python import restrictions...\n")
    sys.stdout.write(f"Blocked modules: {len(BLOCKED_MODULES)}\n")

    # Test blocking
    try:
        import socket
        sys.stdout.write("ERROR: socket import was not blocked!\n")
    except (ImportError, WormImportError) as e:
        sys.stdout.write(f"✓ socket correctly blocked: {type(e).__name__}\n")

    # Test allowed imports
    try:
        import json
        sys.stdout.write("✓ json import allowed\n")
    except ImportError as e:
        sys.stdout.write(f"ERROR: json import failed: {e}\n")

    try:
        import sys
        sys.stdout.write("✓ sys import allowed\n")
    except ImportError as e:
        sys.stdout.write(f"ERROR: sys import failed: {e}\n")
