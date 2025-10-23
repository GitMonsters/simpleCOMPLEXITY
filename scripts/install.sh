#!/bin/bash
# Installation script for Worm Python

set -e

echo "Installing Worm Python..."

# Determine installation directory
if [ "$EUID" -eq 0 ]; then
    INSTALL_DIR="/usr/local/lib/worm-python"
    BIN_DIR="/usr/local/bin"
    echo "Installing system-wide (requires root)"
else
    INSTALL_DIR="$HOME/.local/lib/worm-python"
    BIN_DIR="$HOME/.local/bin"
    echo "Installing for current user"
fi

# Create installation directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

# Copy worm source files
echo "Copying Worm Python files..."
cp -r src/worm/* "$INSTALL_DIR/"

# Make worm.py executable
chmod +x "$INSTALL_DIR/worm.py"

# Create wrapper script in bin directory
echo "Creating worm executable..."
cat > "$BIN_DIR/worm" << 'EOF'
#!/bin/bash
# Worm Python wrapper script

# Determine installation directory
if [ -d "/usr/local/lib/worm-python" ]; then
    WORM_DIR="/usr/local/lib/worm-python"
elif [ -d "$HOME/.local/lib/worm-python" ]; then
    WORM_DIR="$HOME/.local/lib/worm-python"
else
    echo "Error: Worm Python not found. Please run install.sh" >&2
    exit 1
fi

# Run worm.py with the system Python
exec python3 "$WORM_DIR/worm.py" "$@"
EOF

chmod +x "$BIN_DIR/worm"

# Check if bin directory is in PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo ""
    echo "WARNING: $BIN_DIR is not in your PATH"
    echo "Add this to your ~/.bashrc or ~/.zshrc:"
    echo "  export PATH=\"$BIN_DIR:\$PATH\""
    echo ""
fi

echo ""
echo "✓ Worm Python installed successfully!"
echo ""
echo "Installation location: $INSTALL_DIR"
echo "Executable: $BIN_DIR/worm"
echo ""
echo "Test the installation:"
echo "  worm --version"
echo "  worm --info"
echo ""
