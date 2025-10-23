#!/bin/bash
# Uninstallation script for Worm Python

set -e

echo "Uninstalling Worm Python..."

# Determine installation directory
if [ -d "/usr/local/lib/worm-python" ]; then
    INSTALL_DIR="/usr/local/lib/worm-python"
    BIN_DIR="/usr/local/bin"
    if [ "$EUID" -ne 0 ]; then
        echo "Error: System-wide installation requires root to uninstall" >&2
        echo "Run: sudo $0" >&2
        exit 1
    fi
elif [ -d "$HOME/.local/lib/worm-python" ]; then
    INSTALL_DIR="$HOME/.local/lib/worm-python"
    BIN_DIR="$HOME/.local/bin"
else
    echo "Worm Python does not appear to be installed"
    exit 0
fi

# Remove installation directory
if [ -d "$INSTALL_DIR" ]; then
    echo "Removing $INSTALL_DIR..."
    rm -rf "$INSTALL_DIR"
fi

# Remove executable
if [ -f "$BIN_DIR/worm" ]; then
    echo "Removing $BIN_DIR/worm..."
    rm -f "$BIN_DIR/worm"
fi

echo ""
echo "✓ Worm Python uninstalled successfully"
echo ""
