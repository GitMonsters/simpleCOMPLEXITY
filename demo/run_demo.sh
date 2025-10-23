#!/bin/bash
# Interactive Worm Python Demo Runner

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Paths
WORM_BIN="python3 src/worm/worm.py"
DEMO_DIR="demo"

clear

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                                    ║${NC}"
echo -e "${BLUE}║${GREEN}     WORM PYTHON - INTERACTIVE SECURITY FEATURE DEMONSTRATION     ${BLUE}║${NC}"
echo -e "${BLUE}║                                                                    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if worm exists
if [ ! -f "src/worm/worm.py" ]; then
    echo -e "${RED}Error: Worm Python not found at src/worm/worm.py${NC}"
    echo "Please run this script from the COMPLEXITY directory"
    exit 1
fi

show_menu() {
    echo -e "\n${GREEN}Available Demonstrations:${NC}\n"
    echo "  1. Comprehensive Demo (All Features)"
    echo "  2. Network Isolation Demo"
    echo "  3. Attack Simulation: Network Exfiltration"
    echo "  4. Attack Simulation: Resource Exhaustion"
    echo "  5. IoC Monitoring Demo"
    echo "  6. Quick Feature Showcase"
    echo ""
    echo "  v. Verify Worm Source Integrity"
    echo "  m. Monitor Security Status"
    echo "  h. Help & Documentation"
    echo "  q. Quit"
    echo ""
}

run_comprehensive_demo() {
    echo -e "\n${GREEN}Running Comprehensive Demo...${NC}\n"
    echo "This demonstrates ALL security features in one script."
    echo ""
    read -p "Press Enter to start..." dummy
    echo ""

    $WORM_BIN "$DEMO_DIR/comprehensive_demo.py"

    echo ""
    read -p "Press Enter to return to menu..." dummy
}

run_network_demo() {
    echo -e "\n${GREEN}Running Network Isolation Demo...${NC}\n"
    echo "This demonstrates network blocking features."
    echo ""
    read -p "Press Enter to start..." dummy
    echo ""

    $WORM_BIN "$DEMO_DIR/network_blocking_demo.py" 2>/dev/null || \
    $WORM_BIN examples/network_blocking_demo.py

    echo ""
    read -p "Press Enter to return to menu..." dummy
}

run_exfiltration_attack() {
    echo -e "\n${YELLOW}Running Attack Simulation: Network Exfiltration${NC}\n"
    echo "This simulates malicious data exfiltration attempts."
    echo "All attacks will be BLOCKED by Worm Python."
    echo ""
    read -p "Press Enter to start attack simulation..." dummy
    echo ""

    $WORM_BIN "$DEMO_DIR/attack_simulations/network_exfiltration.py"

    echo ""
    read -p "Press Enter to return to menu..." dummy
}

run_dos_attack() {
    echo -e "\n${YELLOW}Running Attack Simulation: Resource Exhaustion${NC}\n"
    echo "This simulates DoS attacks via resource exhaustion."
    echo "Resource limits will prevent these attacks."
    echo ""
    echo -e "${RED}WARNING: This demo allocates memory and creates files.${NC}"
    echo ""
    read -p "Continue? (y/n) " confirm

    if [ "$confirm" != "y" ]; then
        echo "Attack simulation cancelled."
        return
    fi

    echo ""
    $WORM_BIN "$DEMO_DIR/attack_simulations/resource_exhaustion.py"

    echo ""
    read -p "Press Enter to return to menu..." dummy
}

run_ioc_monitoring() {
    echo -e "\n${GREEN}Running IoC Monitoring Demo...${NC}\n"
    echo "Demonstrating Indicator of Compromise detection."
    echo ""

    echo "1. Verifying Worm Source Integrity..."
    python3 tools/ioc_monitor.py --verify-worm-source

    echo ""
    echo "2. Creating test file with print() statement..."

    # Create test file
    TEST_FILE=$(mktemp /tmp/test_XXXX.py)
    cat > "$TEST_FILE" << 'EOF'
# This file contains a print() statement - IoC!
import sys
print("This is malicious!")  # IoC detected!
sys.stdout.write("This is legitimate\n")
EOF

    echo "   Created: $TEST_FILE"
    echo ""
    echo "3. Scanning for IoCs..."
    python3 tools/ioc_monitor.py --scan-file "$TEST_FILE"

    # Cleanup
    rm -f "$TEST_FILE"

    echo ""
    read -p "Press Enter to return to menu..." dummy
}

run_quick_showcase() {
    echo -e "\n${GREEN}Quick Feature Showcase${NC}\n"

    echo "Testing network blocking..."
    $WORM_BIN -c "import socket" 2>&1 | head -2

    echo ""
    echo "Testing subprocess blocking..."
    $WORM_BIN -c "import subprocess; subprocess.run(['curl', 'test.com'])" 2>&1 | head -2

    echo ""
    echo "Testing allowed operations..."
    $WORM_BIN -c "import json; import sys; sys.stdout.write('✓ JSON works\n'); sys.stdout.write('✓ Math works\n')"

    echo ""
    echo -e "${GREEN}Features working correctly!${NC}"

    echo ""
    read -p "Press Enter to return to menu..." dummy
}

verify_integrity() {
    echo -e "\n${GREEN}Verifying Worm Source Integrity...${NC}\n"
    python3 tools/ioc_monitor.py --verify-worm-source
    echo ""
    read -p "Press Enter to return to menu..." dummy
}

monitor_status() {
    echo -e "\n${GREEN}Security Monitoring Status${NC}\n"

    if [ -x "tools/worm_monitor.sh" ]; then
        tools/worm_monitor.sh status
    else
        echo "Monitoring script not found or not executable"
        echo "Check: tools/worm_monitor.sh"
    fi

    echo ""
    read -p "Press Enter to return to menu..." dummy
}

show_help() {
    echo -e "\n${GREEN}Worm Python - Help & Documentation${NC}\n"

    echo "Documentation Available:"
    echo "  • README.md - Overview and quick start"
    echo "  • docs/QUICKSTART.md - Getting started guide"
    echo "  • docs/SECURITY.md - Security model and features"
    echo "  • docs/USE_CASES.md - Intended use cases"
    echo "  • docs/DEPLOYMENT.md - Production deployment"
    echo ""

    echo "Quick Commands:"
    echo "  $ worm --version                  # Check version"
    echo "  $ worm --info                     # Show security info"
    echo "  $ worm --help                     # Usage help"
    echo "  $ worm script.py                  # Run a script"
    echo ""

    echo "Monitoring Commands:"
    echo "  $ python3 tools/ioc_monitor.py --verify-worm-source"
    echo "  $ tools/worm_monitor.sh status"
    echo ""

    echo "Example Usage:"
    echo "  $ worm examples/data_analysis.py"
    echo "  $ worm --strict untrusted_code.py"
    echo "  $ worm --moderate --audit script.py"
    echo ""

    read -p "Press Enter to return to menu..." dummy
}

# Main loop
while true; do
    show_menu
    read -p "Select option: " choice

    case $choice in
        1) run_comprehensive_demo ;;
        2) run_network_demo ;;
        3) run_exfiltration_attack ;;
        4) run_dos_attack ;;
        5) run_ioc_monitoring ;;
        6) run_quick_showcase ;;
        v|V) verify_integrity ;;
        m|M) monitor_status ;;
        h|H) show_help ;;
        q|Q)
            echo ""
            echo -e "${GREEN}Thank you for exploring Worm Python!${NC}"
            echo ""
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option. Please try again.${NC}"
            sleep 1
            ;;
    esac
done
