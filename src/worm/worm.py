#!/usr/bin/env python3
"""
Worm Python - Security Hardened Python Distribution

Main launcher that sets up security restrictions and then runs Python
with network isolation and vulnerability mitigations.
"""

import sys
import os


def setup_worm_environment():
    """
    Set up the Worm Python environment with all security restrictions.

    This must be called before any user code runs.
    """
    # Add worm modules to the path
    worm_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, worm_dir)

    # Install import restrictions
    from hooks.import_restrictions import install_import_restrictions
    install_import_restrictions()

    # Replace subprocess with restricted version
    from modules import restricted_subprocess
    sys.modules['subprocess'] = restricted_subprocess

    # Set environment variables to indicate we're running in Worm
    os.environ['WORM_PYTHON'] = '1'
    os.environ['PYTHON_SECURE_MODE'] = '1'


def show_worm_info():
    """Display information about Worm Python."""
    print("Worm Python - Security Hardened Python Distribution")
    print(f"Based on Python {sys.version}")
    print()
    print("Security Features:")
    print("  ✓ Network access disabled (socket, urllib, requests, etc.)")
    print("  ✓ Network commands blocked in subprocess")
    print("  ✓ Import restrictions enforced")
    print()
    print("Use 'worm --help' for usage information")
    print()


def show_help():
    """Show help information."""
    print("Worm Python - Security Hardened Python Distribution")
    print()
    print("Usage:")
    print("  worm                  Start interactive REPL")
    print("  worm script.py        Run a Python script")
    print("  worm -m module        Run a module as a script")
    print("  worm -c 'code'        Execute Python code")
    print("  worm --info           Show Worm Python information")
    print("  worm --help           Show this help message")
    print("  worm --version        Show version information")
    print()
    print("Security Features:")
    print("  • All network modules are disabled (socket, urllib, http, etc.)")
    print("  • Network commands are blocked in subprocess")
    print("  • Standard I/O and file operations work normally")
    print("  • All non-network Python features are available")
    print()


def main():
    """Main entry point for Worm Python."""
    # Check for special flags before setting up restrictions
    if len(sys.argv) > 1:
        if sys.argv[1] == '--help':
            show_help()
            return 0
        elif sys.argv[1] == '--info':
            show_worm_info()
            return 0
        elif sys.argv[1] == '--version':
            print(f"Worm Python 0.1.0-alpha (based on Python {sys.version.split()[0]})")
            return 0

    # Set up security restrictions
    setup_worm_environment()

    # Print banner for interactive mode
    if len(sys.argv) == 1:
        print("Worm Python 0.1.0-alpha (Security Hardened)")
        print(f"Based on Python {sys.version.split()[0]}")
        print('Type "help", "copyright", "credits" or "license" for more information.')
        print("Network access is DISABLED in this Python distribution.")
        print()

    # Now run Python normally with our restrictions in place
    # The restrictions are already installed via setup_worm_environment()

    # Handle different invocation modes
    if len(sys.argv) == 1:
        # Interactive mode - start REPL
        import code
        code.interact(banner='', local=globals())
    elif sys.argv[1] == '-c':
        # Execute code from command line
        if len(sys.argv) < 3:
            print("Error: -c requires code argument", file=sys.stderr)
            return 1
        code = sys.argv[2]
        exec(code, {'__name__': '__main__'})
    elif sys.argv[1] == '-m':
        # Run module as script
        if len(sys.argv) < 3:
            print("Error: -m requires module name", file=sys.stderr)
            return 1
        module_name = sys.argv[2]
        # Remove worm args and set up sys.argv for the module
        sys.argv = [module_name] + sys.argv[3:]
        import runpy
        runpy.run_module(module_name, run_name='__main__')
    else:
        # Run script file
        script_path = sys.argv[1]
        if not os.path.exists(script_path):
            print(f"Error: can't open file '{script_path}': No such file or directory", file=sys.stderr)
            return 2

        # Set up sys.argv for the script
        sys.argv = sys.argv[1:]

        # Read and execute the script
        with open(script_path, 'r') as f:
            code = f.read()

        # Set __file__ and __name__ appropriately
        globals_dict = {
            '__name__': '__main__',
            '__file__': os.path.abspath(script_path),
        }

        exec(compile(code, script_path, 'exec'), globals_dict)

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
