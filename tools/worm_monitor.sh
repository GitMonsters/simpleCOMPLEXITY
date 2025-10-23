#!/bin/bash
# Worm Python Security Monitor
# Continuously monitors for security events and IoCs

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default log file
LOG_FILE="${HOME}/.worm/audit.log"
MONITOR_SCRIPT="$(dirname "$0")/ioc_monitor.py"

echo "======================================"
echo "Worm Python Security Monitor"
echo "======================================"
echo ""

# Check if audit log exists
if [ ! -f "$LOG_FILE" ]; then
    echo -e "${YELLOW}⚠  Audit log not found: $LOG_FILE${NC}"
    echo "   Run Worm Python with audit logging enabled first"
    echo ""
fi

# Function to check for print() in running processes
check_running_processes() {
    echo -e "${GREEN}Checking running Python processes...${NC}"

    # Find Python processes
    pids=$(pgrep -f "python.*worm" || true)

    if [ -z "$pids" ]; then
        echo "  No Worm Python processes found"
        return
    fi

    for pid in $pids; then
        # Check if process is actually worm
        if [ -f "/proc/$pid/cmdline" ]; then
            cmdline=$(tr '\0' ' ' < /proc/$pid/cmdline 2>/dev/null || true)
            if [[ "$cmdline" == *"worm"* ]]; then
                echo -e "  ${GREEN}✓${NC} Worm process: PID $pid"
            fi
        fi
    done
}

# Function to verify Worm source integrity
verify_source() {
    echo -e "${GREEN}Verifying Worm Python source integrity...${NC}"

    if [ -x "$MONITOR_SCRIPT" ]; then
        python3 "$MONITOR_SCRIPT" --verify-worm-source
    else
        echo -e "${YELLOW}⚠  Monitor script not found${NC}"
    fi
}

# Function to show recent audit events
show_recent_events() {
    echo -e "${GREEN}Recent audit events:${NC}"

    if [ -f "$LOG_FILE" ]; then
        tail -10 "$LOG_FILE" | while IFS= read -r line; do
            # Parse JSON and extract event type
            event_type=$(echo "$line" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('event_type', 'unknown'))" 2>/dev/null || echo "unknown")

            if [[ "$event_type" == "IOC_DETECTED" ]]; then
                echo -e "  ${RED}⚠  CRITICAL: $event_type${NC}"
            elif [[ "$event_type" == "blocked_"* ]]; then
                echo -e "  ${YELLOW}✓ $event_type${NC}"
            else
                echo "  • $event_type"
            fi
        done
    else
        echo "  No audit log found"
    fi
}

# Function to count security events
count_events() {
    echo -e "${GREEN}Security event summary:${NC}"

    if [ ! -f "$LOG_FILE" ]; then
        echo "  No audit log found"
        return
    fi

    total=$(wc -l < "$LOG_FILE")
    blocked_imports=$(grep -c '"event_type": "blocked_import"' "$LOG_FILE" || true)
    blocked_subprocess=$(grep -c '"event_type": "blocked_subprocess"' "$LOG_FILE" || true)
    iocs=$(grep -c '"event_type": "IOC_DETECTED"' "$LOG_FILE" || true)

    echo "  Total events: $total"
    echo "  Blocked imports: $blocked_imports"
    echo "  Blocked subprocesses: $blocked_subprocess"

    if [ "$iocs" -gt 0 ]; then
        echo -e "  ${RED}⚠  CRITICAL - IoCs detected: $iocs${NC}"
    else
        echo -e "  ${GREEN}✓ IoCs detected: 0${NC}"
    fi
}

# Main monitoring loop
case "${1:-status}" in
    status)
        echo ""
        verify_source
        echo ""
        check_running_processes
        echo ""
        count_events
        echo ""
        show_recent_events
        echo ""
        ;;

    follow)
        echo "Monitoring audit log in real-time (Ctrl+C to stop)..."
        echo "Log file: $LOG_FILE"
        echo ""

        if [ -x "$MONITOR_SCRIPT" ]; then
            python3 "$MONITOR_SCRIPT" --monitor-log --follow
        else
            # Fallback to tail
            tail -f "$LOG_FILE" 2>/dev/null | while IFS= read -r line; do
                if [[ "$line" == *"IOC_DETECTED"* ]]; then
                    echo -e "${RED}⚠  CRITICAL: $line${NC}"
                else
                    echo "$line"
                fi
            done
        fi
        ;;

    verify)
        verify_source
        ;;

    help|--help|-h)
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  status    Show current security status (default)"
        echo "  follow    Monitor audit log in real-time"
        echo "  verify    Verify Worm Python source integrity"
        echo "  help      Show this help message"
        echo ""
        ;;

    *)
        echo "Unknown command: $1"
        echo "Run '$0 help' for usage information"
        exit 1
        ;;
esac
