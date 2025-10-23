"""
Filesystem sandboxing for Worm Python

Provides optional restrictions on file system access,
including read-only mode and directory whitelisting.
"""

import sys
import os
import builtins
from pathlib import Path


class FilesystemAccessError(Exception):
    """Raised when file system access is denied by sandbox."""
    pass


class FilesystemSandbox:
    """
    Filesystem sandbox for restricting file access.

    Can operate in different modes:
    - read_only: Only read operations allowed
    - whitelist: Only access files in specific directories
    - blacklist: Deny access to specific directories
    """

    def __init__(self, mode='disabled', allowed_paths=None, denied_paths=None):
        """
        Initialize filesystem sandbox.

        Args:
            mode: Sandbox mode ('disabled', 'read_only', 'whitelist', 'blacklist')
            allowed_paths: List of allowed paths (for whitelist mode)
            denied_paths: List of denied paths (for blacklist mode)
        """
        self.mode = mode
        self.allowed_paths = [Path(p).resolve() for p in (allowed_paths or [])]
        self.denied_paths = [Path(p).resolve() for p in (denied_paths or [])]
        self.original_open = builtins.open
        self.enabled = False

    def _is_path_allowed(self, filepath):
        """Check if path is allowed by sandbox rules."""
        try:
            filepath = Path(filepath).resolve()
        except:
            # If we can't resolve the path, deny it
            return False

        # Check blacklist
        if self.mode == 'blacklist':
            for denied in self.denied_paths:
                try:
                    filepath.relative_to(denied)
                    return False  # Path is under denied directory
                except ValueError:
                    continue  # Path is not under this denied directory
            return True  # Not in blacklist, allow

        # Check whitelist
        if self.mode == 'whitelist':
            for allowed in self.allowed_paths:
                try:
                    filepath.relative_to(allowed)
                    return True  # Path is under allowed directory
                except ValueError:
                    continue  # Path is not under this allowed directory
            return False  # Not in whitelist, deny

        # Read-only mode allows all reads
        if self.mode == 'read_only':
            return True

        # Disabled mode allows everything
        return True

    def _sandboxed_open(self, file, mode='r', *args, **kwargs):
        """Sandboxed version of open()."""
        # Check if write mode
        is_write = any(m in mode for m in ['w', 'a', 'x', '+'])

        # In read-only mode, deny writes
        if self.mode == 'read_only' and is_write:
            raise FilesystemAccessError(
                f"File system is in read-only mode. "
                f"Write access to '{file}' denied."
            )

        # Check path permissions
        if not self._is_path_allowed(file):
            raise FilesystemAccessError(
                f"Access to '{file}' denied by filesystem sandbox. "
                f"Path is not in allowed list."
            )

        # If we get here, access is allowed
        return self.original_open(file, mode, *args, **kwargs)

    def enable(self):
        """Enable the filesystem sandbox."""
        if self.mode == 'disabled':
            return False

        builtins.open = self._sandboxed_open
        self.enabled = True
        return True

    def disable(self):
        """Disable the filesystem sandbox."""
        builtins.open = self.original_open
        self.enabled = False

    def get_status(self):
        """Get sandbox status."""
        return {
            'enabled': self.enabled,
            'mode': self.mode,
            'allowed_paths': [str(p) for p in self.allowed_paths],
            'denied_paths': [str(p) for p in self.denied_paths],
        }


# Global sandbox instance
_sandbox = None


def enable_filesystem_sandbox(mode='read_only', allowed_paths=None, denied_paths=None):
    """
    Enable filesystem sandbox globally.

    Args:
        mode: Sandbox mode
        allowed_paths: List of allowed paths (whitelist mode)
        denied_paths: List of denied paths (blacklist mode)

    Returns:
        FilesystemSandbox: The sandbox instance
    """
    global _sandbox
    _sandbox = FilesystemSandbox(mode=mode, allowed_paths=allowed_paths, denied_paths=denied_paths)
    _sandbox.enable()
    return _sandbox


def disable_filesystem_sandbox():
    """Disable filesystem sandbox."""
    global _sandbox
    if _sandbox:
        _sandbox.disable()


def get_sandbox_status():
    """Get current sandbox status."""
    if _sandbox:
        return _sandbox.get_status()
    return {'enabled': False, 'mode': 'disabled'}


if __name__ == '__main__':
    import tempfile

    sys.stdout.write("Testing filesystem sandbox...\n\n")

    # Create test file
    test_dir = Path(tempfile.mkdtemp())
    test_file = test_dir / 'test.txt'

    sys.stdout.write(f"Test directory: {test_dir}\n\n")

    # Test 1: Read-only mode
    sys.stdout.write("Test 1: Read-only mode\n")
    sandbox = FilesystemSandbox(mode='read_only')
    sandbox.enable()

    try:
        # This should fail (write in read-only mode)
        with open(test_file, 'w') as f:
            f.write('test')
        sys.stdout.write("  ERROR: Write was not blocked!\n")
    except FilesystemAccessError:
        sys.stdout.write("  ✓ Write blocked in read-only mode\n")

    sandbox.disable()

    # Create the file for next test
    with open(test_file, 'w') as f:
        f.write('test data')

    # Test 2: Whitelist mode
    sys.stdout.write("\nTest 2: Whitelist mode\n")
    sandbox = FilesystemSandbox(mode='whitelist', allowed_paths=[str(test_dir)])
    sandbox.enable()

    try:
        # This should work (in whitelist)
        with open(test_file, 'r') as f:
            data = f.read()
        sys.stdout.write(f"  ✓ Read allowed: '{data}'\n")
    except FilesystemAccessError:
        sys.stdout.write("  ERROR: Read was blocked!\n")

    try:
        # This should fail (not in whitelist)
        with open('/tmp/other_file.txt', 'w') as f:
            f.write('test')
        sys.stdout.write("  ERROR: Access to non-whitelisted path was allowed!\n")
    except FilesystemAccessError:
        sys.stdout.write("  ✓ Access to non-whitelisted path blocked\n")

    sandbox.disable()

    # Test 3: Blacklist mode
    sys.stdout.write("\nTest 3: Blacklist mode\n")
    denied_dir = Path(tempfile.mkdtemp())
    sandbox = FilesystemSandbox(mode='blacklist', denied_paths=[str(denied_dir)])
    sandbox.enable()

    try:
        # This should fail (in blacklist)
        denied_file = denied_dir / 'blocked.txt'
        with open(denied_file, 'w') as f:
            f.write('test')
        sys.stdout.write("  ERROR: Access to blacklisted path was allowed!\n")
    except FilesystemAccessError:
        sys.stdout.write("  ✓ Access to blacklisted path blocked\n")

    sandbox.disable()

    # Cleanup
    import shutil
    shutil.rmtree(test_dir)
    shutil.rmtree(denied_dir)

    sys.stdout.write("\n✓ Filesystem sandbox test complete\n")
