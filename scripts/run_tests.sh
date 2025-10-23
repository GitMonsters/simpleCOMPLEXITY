#!/bin/bash
# Run all tests for Worm Python

set -e

echo "Running Worm Python Test Suite"
echo "==============================="
echo ""

# Check if pytest is installed
if ! python3 -c "import pytest" 2>/dev/null; then
    echo "Installing pytest..."
    pip3 install pytest
fi

# Run tests
echo "Running unit tests..."
python3 -m pytest tests/ -v --tb=short

echo ""
echo "==============================="
echo "All tests completed!"
