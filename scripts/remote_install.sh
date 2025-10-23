#!/bin/bash
# Worm Python - One-Command Installation Script
# Run this on your home machine: bash install_worm.sh

set -e

echo "============================================"
echo "Worm Python Installation"
echo "============================================"
echo ""

# Check if git is available
if ! command -v git &> /dev/null; then
    echo "Installing git..."
    sudo apt-get update && sudo apt-get install -y git
fi

# Clone repository
echo "Cloning Worm Python repository..."
cd ~
if [ -d "COMPLEXITY" ]; then
    echo "Repository already exists, updating..."
    cd COMPLEXITY
    git fetch origin
else
    git clone https://github.com/GitMonsters/COMPLEXITY.git
    cd COMPLEXITY
fi

# Switch to the correct branch
echo "Switching to development branch..."
git checkout claude/create-test-branch-011CUMhAyjZeoPTf9EWYHRE3
git pull origin claude/create-test-branch-011CUMhAyjZeoPTf9EWYHRE3

# Install Worm Python
echo ""
echo "Installing Worm Python..."
./scripts/install.sh

# Verify installation
echo ""
echo "============================================"
echo "Installation Complete!"
echo "============================================"
echo ""

worm --version
worm --info

echo ""
echo "Try it out:"
echo "  worm examples/network_blocking_demo.py"
echo "  ./demo/run_demo.sh"
echo ""
echo "Documentation:"
echo "  docs/QUICKSTART.md"
echo "  docs/DEPLOYMENT.md"
echo ""
