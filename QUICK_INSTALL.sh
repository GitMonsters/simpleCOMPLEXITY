#!/bin/bash

# COMPLEXITY Project - Quick Installation Script
# This script sets up the COMPLEXITY project environment

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_info "Starting COMPLEXITY project installation..."

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if git is installed
if ! command -v git &> /dev/null; then
    print_error "git is not installed. Please install git first."
    exit 1
fi

print_info "Git found: $(git --version)"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    print_error "Not in a git repository. Please clone the repository first."
    exit 1
fi

print_info "Git repository detected"

# Pull latest changes
print_info "Pulling latest changes from repository..."
git pull origin "$(git branch --show-current)" || print_warn "Could not pull latest changes (might be offline or up to date)"

# Check for common dependencies
print_info "Checking system dependencies..."

# Check for Python
if command -v python3 &> /dev/null; then
    print_info "Python3 found: $(python3 --version)"
else
    print_warn "Python3 not found"
fi

# Check for Node.js
if command -v node &> /dev/null; then
    print_info "Node.js found: $(node --version)"
else
    print_warn "Node.js not found"
fi

# Check for Docker
if command -v docker &> /dev/null; then
    print_info "Docker found: $(docker --version)"
else
    print_warn "Docker not found"
fi

# Create common directories if they don't exist
print_info "Setting up project structure..."
mkdir -p data logs config

# Set permissions
chmod +x "$0"

print_info "Installation directory: $SCRIPT_DIR"
print_info "Current branch: $(git branch --show-current)"
print_info "Latest commit: $(git log -1 --oneline)"

echo ""
print_info "${GREEN}Installation completed successfully!${NC}"
echo ""
echo "To get started:"
echo "  1. Review the README.md for detailed instructions"
echo "  2. Configure your settings in the config/ directory"
echo "  3. Check the documentation for usage examples"
echo ""
print_info "Project location: $SCRIPT_DIR"
