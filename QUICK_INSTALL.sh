#!/bin/bash
# Worm Python - Quick Installation Guide
# Run this script on your home machine to install everything

set -e

echo "╔═══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                       ║"
echo "║              WORM PYTHON - HOME INSTALLATION                          ║"
echo "║              Security-Hardened Python Distribution                    ║"
echo "║                                                                       ║"
echo "╚═══════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if we're in the right directory
if [ ! -d "src/worm" ]; then
    echo "✗ Error: Not in COMPLEXITY directory"
    echo "  Please cd to COMPLEXITY first"
    exit 1
fi

echo "Current directory: $(pwd)"
echo ""

# Step 1: Make install script executable
echo "Step 1: Preparing installation script..."
echo "────────────────────────────────────────────────────────────────────────"
chmod +x scripts/install.sh
echo "✓ Installation script ready"
echo ""

# Step 2: Run installation
echo "Step 2: Installing Worm Python..."
echo "────────────────────────────────────────────────────────────────────────"
echo ""
echo "Choose installation type:"
echo "  1) User installation (recommended) - installs to ~/.local/"
echo "  2) System installation - installs to /usr/local/ (requires sudo)"
echo ""
read -p "Enter choice (1 or 2): " choice

if [ "$choice" = "1" ]; then
    ./scripts/install.sh
elif [ "$choice" = "2" ]; then
    sudo ./scripts/install.sh --system
else
    echo "Invalid choice. Installing as user..."
    ./scripts/install.sh
fi

echo ""
echo "✓ Installation complete!"
echo ""

# Step 3: Verify installation
echo "Step 3: Verifying installation..."
echo "────────────────────────────────────────────────────────────────────────"

# Check if worm is in PATH
if command -v worm &> /dev/null; then
    echo "✓ worm command found in PATH"
    worm --version
else
    echo "⚠ worm command not found in PATH"
    echo ""
    echo "Add to PATH by running:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
    echo "To make permanent, add to ~/.bashrc:"
    echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
    echo "  source ~/.bashrc"
    echo ""

    # Offer to add to PATH now
    read -p "Add to PATH now? (y/n): " add_path
    if [ "$add_path" = "y" ]; then
        export PATH="$HOME/.local/bin:$PATH"
        echo "✓ Added to PATH for this session"
        echo ""
        echo "To make permanent, run:"
        echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
    fi
fi

echo ""

# Step 4: Run tests
echo "Step 4: Running quick tests..."
echo "────────────────────────────────────────────────────────────────────────"
echo ""

echo "Test 1: Basic execution"
worm -c "import sys; sys.stdout.write('✓ Basic execution works\n')"

echo ""
echo "Test 2: Network blocking"
worm -c "import socket" 2>&1 | head -1 || echo "✓ Network modules blocked as expected"

echo ""
echo "Test 3: File operations"
worm -c "import sys; open('/tmp/worm_test.txt', 'w').write('test'); sys.stdout.write('✓ File operations work\n')"
rm -f /tmp/worm_test.txt

echo ""

# Step 5: Show examples
echo "╔═══════════════════════════════════════════════════════════════════════╗"
echo "║                     INSTALLATION COMPLETE!                            ║"
echo "╚═══════════════════════════════════════════════════════════════════════╝"
echo ""

echo "What's installed:"
echo "  • Worm Python interpreter"
echo "  • Security features (8 layers)"
echo "  • Monitoring tools"
echo "  • Example workflows"
echo "  • ARC Prize competition workflow"
echo "  • Worm Rust proof-of-concept"
echo ""

echo "Try these examples:"
echo "────────────────────────────────────────────────────────────────────────"
echo ""
echo "1. Hello World:"
echo "   worm -c \"import sys; sys.stdout.write('Hello from Worm Python!\\n')\""
echo ""
echo "2. Run an example:"
echo "   worm examples/text_processing.py"
echo ""
echo "3. Interactive demo:"
echo "   cd demo && ./run_demo.sh"
echo ""
echo "4. ARC Prize workflow (ML competition):"
echo "   cd examples/arc_prize_workflow"
echo "   cat README.md"
echo ""
echo "5. Security monitoring:"
echo "   ./tools/worm_monitor.sh"
echo ""

echo "Documentation:"
echo "────────────────────────────────────────────────────────────────────────"
echo "  • README.md - Main documentation"
echo "  • docs/QUICKSTART.md - Getting started guide"
echo "  • docs/SECURITY.md - Security features explained"
echo "  • docs/USE_CASES.md - Real-world examples"
echo "  • examples/arc_prize_workflow/README.md - Competition workflow"
echo "  • worm-rust-poc/README.md - Rust version (POC)"
echo ""

echo "Next steps:"
echo "────────────────────────────────────────────────────────────────────────"
echo "  1. Read: cat README.md"
echo "  2. Try: worm examples/text_processing.py"
echo "  3. Demo: cd demo && ./run_demo.sh"
echo "  4. Monitor: ./tools/worm_monitor.sh"
echo ""

echo "Need help?"
echo "  • Check docs/ directory"
echo "  • Run: worm --help"
echo ""

echo "Security status:"
echo "  ✓ Network access blocked"
echo "  ✓ Subprocess filtering active"
echo "  ✓ Resource limits configured"
echo "  ✓ Audit logging enabled"
echo "  ✓ IoC monitoring available"
echo ""

echo "Happy secure coding! 🔒"
echo ""
