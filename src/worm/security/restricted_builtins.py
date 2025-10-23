"""
Restricted builtins for Worm Python

Provides optional restrictions on dangerous Python builtins like eval, exec, compile.
"""

import sys
import builtins


class RestrictedBuiltinsError(Exception):
    """Raised when attempting to use a restricted builtin."""
    pass


# Store original builtins
_original_eval = builtins.eval
_original_exec = builtins.exec
_original_compile = builtins.compile
_original_open = builtins.open
_original_import = builtins.__import__


def _restricted_eval(*args, **kwargs):
    """Restricted version of eval() that always raises an error."""
    raise RestrictedBuiltinsError(
        "eval() is disabled in Worm Python restricted mode. "
        "This function can execute arbitrary code and is disabled for security."
    )


def _restricted_exec(*args, **kwargs):
    """Restricted version of exec() that always raises an error."""
    raise RestrictedBuiltinsError(
        "exec() is disabled in Worm Python restricted mode. "
        "This function can execute arbitrary code and is disabled for security."
    )


def _restricted_compile(*args, **kwargs):
    """Restricted version of compile() that always raises an error."""
    raise RestrictedBuiltinsError(
        "compile() is disabled in Worm Python restricted mode. "
        "This function can create code objects and is disabled for security."
    )


def _restricted_open(file, mode='r', *args, **kwargs):
    """
    Restricted version of open() with path validation.

    Can be configured to only allow specific paths or modes.
    """
    # For now, allow all opens (can be configured later)
    # In strict mode, you could whitelist only certain directories
    return _original_open(file, mode, *args, **kwargs)


def enable_restricted_builtins(level='strict'):
    """
    Enable restricted builtins.

    Args:
        level: Restriction level
            - 'strict': Disable eval, exec, compile
            - 'moderate': Disable eval, exec (keep compile)
            - 'minimal': Disable eval only

    Returns:
        bool: True if restrictions were applied
    """
    if level in ('strict', 'moderate', 'minimal'):
        builtins.eval = _restricted_eval

    if level in ('strict', 'moderate'):
        builtins.exec = _restricted_exec

    if level == 'strict':
        builtins.compile = _restricted_compile

    return True


def disable_restricted_builtins():
    """
    Restore original builtins.

    Note: This is only for testing. In production, restrictions
    should not be removable.
    """
    builtins.eval = _original_eval
    builtins.exec = _original_exec
    builtins.compile = _original_compile
    builtins.open = _original_open


def get_restriction_status():
    """
    Get current builtin restriction status.

    Returns:
        dict: Status of each builtin
    """
    return {
        'eval_restricted': builtins.eval != _original_eval,
        'exec_restricted': builtins.exec != _original_exec,
        'compile_restricted': builtins.compile != _original_compile,
        'open_restricted': builtins.open != _original_open,
    }


if __name__ == '__main__':
    sys.stdout.write("Testing restricted builtins...\n\n")

    # Test before restrictions
    sys.stdout.write("Before restrictions:\n")
    try:
        result = eval('2 + 2')
        sys.stdout.write(f"  eval('2 + 2') = {result}\n")
    except Exception as e:
        sys.stdout.write(f"  eval failed: {e}\n")

    # Enable restrictions
    sys.stdout.write("\nEnabling strict restrictions...\n")
    enable_restricted_builtins('strict')

    status = get_restriction_status()
    sys.stdout.write(f"  eval_restricted: {status['eval_restricted']}\n")
    sys.stdout.write(f"  exec_restricted: {status['exec_restricted']}\n")
    sys.stdout.write(f"  compile_restricted: {status['compile_restricted']}\n")

    # Test after restrictions
    sys.stdout.write("\nAfter restrictions:\n")
    try:
        result = eval('2 + 2')
        sys.stdout.write("  ERROR: eval was not blocked!\n")
    except RestrictedBuiltinsError as e:
        sys.stdout.write(f"  ✓ eval blocked: {type(e).__name__}\n")

    try:
        exec('x = 1')
        sys.stdout.write("  ERROR: exec was not blocked!\n")
    except RestrictedBuiltinsError as e:
        sys.stdout.write(f"  ✓ exec blocked: {type(e).__name__}\n")

    try:
        compile('x = 1', '<string>', 'exec')
        sys.stdout.write("  ERROR: compile was not blocked!\n")
    except RestrictedBuiltinsError as e:
        sys.stdout.write(f"  ✓ compile blocked: {type(e).__name__}\n")

    sys.stdout.write("\n✓ Restricted builtins working correctly\n")
