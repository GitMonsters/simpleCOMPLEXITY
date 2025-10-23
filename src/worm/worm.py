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
    sys.stdout.write("Worm Python - Security Hardened Python Distribution\n")
    sys.stdout.write(f"Based on Python {sys.version}\n")
    sys.stdout.write("\n")
    sys.stdout.write("Security Features:\n")
    sys.stdout.write("  ✓ Network access disabled (socket, urllib, requests, etc.)\n")
    sys.stdout.write("  ✓ Network commands blocked in subprocess\n")
    sys.stdout.write("  ✓ Import restrictions enforced\n")
    sys.stdout.write("\n")
    sys.stdout.write("Use 'worm --help' for usage information\n")
    sys.stdout.write("\n")


def show_help():
    """Show help information."""
    sys.stdout.write("Worm Python - Security Hardened Python Distribution\n")
    sys.stdout.write("\n")
    sys.stdout.write("Usage:\n")
    sys.stdout.write("  worm                  Start interactive REPL\n")
    sys.stdout.write("  worm script.py        Run a Python script\n")
    sys.stdout.write("  worm -m module        Run a module as a script\n")
    sys.stdout.write("  worm -c 'code'        Execute Python code\n")
    sys.stdout.write("  worm --info           Show Worm Python information\n")
    sys.stdout.write("  worm --help           Show this help message\n")
    sys.stdout.write("  worm --version        Show version information\n")
    sys.stdout.write("\n")
    sys.stdout.write("Security Features:\n")
    sys.stdout.write("  • All network modules are disabled (socket, urllib, http, etc.)\n")
    sys.stdout.write("  • Network commands are blocked in subprocess\n")
    sys.stdout.write("  • Standard I/O and file operations work normally\n")
    sys.stdout.write("  • All non-network Python features are available\n")
    sys.stdout.write("\n")


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
            sys.stdout.write(f"Worm Python 0.1.0-alpha (based on Python {sys.version.split()[0]})\n")
            return 0

    # Set up security restrictions
    setup_worm_environment()

    # Print banner for interactive mode
    if len(sys.argv) == 1:
        sys.stdout.write("Worm Python 0.1.0-alpha (Security Hardened)\n")
        sys.stdout.write(f"Based on Python {sys.version.split()[0]}\n")
        sys.stdout.write('Type "help", "copyright", "credits" or "license" for more information.\n')
        sys.stdout.write("Network access is DISABLED in this Python distribution.\n")
        sys.stdout.write("\n")

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
            sys.stderr.write("Error: -c requires code argument\n")
            return 1
        code = sys.argv[2]
        exec(code, {'__name__': '__main__'})
    elif sys.argv[1] == '-m':
        # Run module as script
        if len(sys.argv) < 3:
            sys.stderr.write("Error: -m requires module name\n")
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
            sys.stderr.write(f"Error: can't open file '{script_path}': No such file or directory\n")
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
        sys.stdout.write("\nKeyboardInterrupt\n")
        sys.exit(130)
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)
