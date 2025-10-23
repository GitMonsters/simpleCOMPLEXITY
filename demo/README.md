# Worm Python Demonstrations

This directory contains comprehensive demonstrations of Worm Python's security features.

## Quick Start

### Interactive Demo

Run the interactive demo launcher:

```bash
./demo/run_demo.sh
```

This provides a menu-driven interface to explore all features.

### Comprehensive Demo

Run the full feature demonstration:

```bash
python3 src/worm/worm.py demo/comprehensive_demo.py
```

This single script demonstrates all 8 security layers in action.

## Available Demonstrations

### 1. Comprehensive Demo (`comprehensive_demo.py`)

**What it shows:**
- All security features in one script
- Print-free codebase (IoC detection)
- Network isolation (3 layers)
- Resource limits
- Restricted builtins
- Filesystem sandboxing
- Audit logging
- Monitoring tools

**Run:**
```bash
python3 src/worm/worm.py demo/comprehensive_demo.py
```

**Duration:** ~30 seconds

---

### 2. Attack Simulations

#### Network Exfiltration (`attack_simulations/network_exfiltration.py`)

**What it shows:**
- Socket-based exfiltration attempts (BLOCKED)
- HTTP data transmission (BLOCKED)
- Curl subprocess exfiltration (BLOCKED)
- DNS tunneling (BLOCKED)

**Run:**
```bash
python3 src/worm/worm.py demo/attack_simulations/network_exfiltration.py
```

**Expected result:** All 4 attack methods blocked

---

#### Resource Exhaustion (`attack_simulations/resource_exhaustion.py`)

**What it shows:**
- Memory exhaustion attempts
- Disk space exhaustion
- File descriptor exhaustion
- CPU exhaustion (infinite loops)

**Run:**
```bash
python3 src/worm/worm.py demo/attack_simulations/resource_exhaustion.py
```

**Expected result:** Attacks limited/prevented with resource limits enabled

**WARNING:** This demo actually allocates memory and creates files. It's designed to be safe but runs real attacks.

---

### 3. Performance Benchmark (`benchmark.py`)

**What it shows:**
- Performance overhead of security features
- Comparison: Standard Python vs Worm Python
- Multiple workload types

**Run:**
```bash
python3 demo/benchmark.py
```

**Duration:** ~1-2 minutes

**Note:** Runs outside Worm Python to measure overhead

---

## Interactive Demo Menu

The `run_demo.sh` script provides an easy-to-use menu:

```
1. Comprehensive Demo (All Features)
2. Network Isolation Demo
3. Attack Simulation: Network Exfiltration
4. Attack Simulation: Resource Exhaustion
5. IoC Monitoring Demo
6. Quick Feature Showcase

v. Verify Worm Source Integrity
m. Monitor Security Status
h. Help & Documentation
q. Quit
```

## Use Cases Demonstrated

### Defensive Security
- Safe execution of untrusted code
- Data exfiltration prevention
- DoS attack mitigation
- Breach detection (IoC monitoring)

### Real-World Scenarios
- Student code submission grading
- Malware analysis sandbox
- Sensitive data processing
- Code competition judging

## Example Workflows

### Scenario 1: Untrusted Code Execution

```bash
# Run untrusted code safely
python3 src/worm/worm.py --strict untrusted_script.py

# Check audit log for violations
python3 tools/ioc_monitor.py --monitor-log
```

### Scenario 2: Sensitive Data Processing

```bash
# Process confidential data with read-only filesystem
python3 src/worm/worm.py --read-only process_data.py

# Verify no data exfiltration
python3 tools/ioc_monitor.py --verify-worm-source
```

### Scenario 3: Attack Analysis

```bash
# Run attack simulation
python3 src/worm/worm.py demo/attack_simulations/network_exfiltration.py

# Review what was blocked
grep "blocked" ~/.worm/audit.log
```

## Testing Matrix

| Feature | Demo Script | Expected Result |
|---------|-------------|-----------------|
| Import blocking | comprehensive_demo.py | socket/urllib/http blocked |
| Subprocess filtering | network_exfiltration.py | curl/wget/ssh blocked |
| Resource limits | resource_exhaustion.py | Memory/CPU limited |
| Restricted builtins | comprehensive_demo.py | eval/exec blocked |
| Filesystem sandbox | comprehensive_demo.py | Writes blocked in read-only |
| Audit logging | comprehensive_demo.py | Events logged to JSON |
| IoC detection | run_demo.sh → option 5 | print() detected |
| Print-free codebase | verify-worm-source | Zero print() found |

## Security Validation

### Verify Integrity

Before running demos, verify Worm Python hasn't been compromised:

```bash
python3 tools/ioc_monitor.py --verify-worm-source
```

**Expected output:**
```
✓ Worm Python source code integrity verified
✓ No print() statements found (as expected)
```

### Monitor During Demos

Run security monitoring while demos execute:

```bash
# Terminal 1: Run demo
python3 src/worm/worm.py demo/comprehensive_demo.py

# Terminal 2: Monitor
tools/worm_monitor.sh follow
```

## Troubleshooting

### Demo won't run

**Problem:** `FileNotFoundError: src/worm/worm.py`

**Solution:** Run from COMPLEXITY directory:
```bash
cd /path/to/COMPLEXITY
./demo/run_demo.sh
```

### Permission denied

**Problem:** `Permission denied: ./demo/run_demo.sh`

**Solution:**
```bash
chmod +x demo/run_demo.sh demo/*.py demo/attack_simulations/*.py
```

### Resource exhaustion demo too aggressive

**Problem:** System becomes unresponsive

**Solution:** The demo is self-limiting. It stops after moderate resource use. If concerned, skip this demo or run in a container.

## Educational Use

These demos are perfect for:

### Classroom Demonstrations
1. Run `comprehensive_demo.py` to show all features (5 min)
2. Run attack simulations to show what's prevented (5 min)
3. Discuss use cases and deployment (10 min)

### Security Training
1. Explain threat model
2. Run network exfiltration attacks
3. Show how each layer prevents bypass
4. Review audit logs

### Conference Talks / Presentations
- Use `run_demo.sh` interactive menu
- Live coding: try to bypass (spoiler: you can't)
- Show monitoring tools in real-time

## Contributing Demos

Want to add a demo? It should:

1. **Demonstrate defensive security** - Show how Worm Python protects
2. **Be safe to run** - Don't actually compromise systems
3. **Use sys.stdout.write()** - Maintain print-free codebase
4. **Include clear output** - Explain what's happening
5. **Be self-contained** - Work standalone

## Demo Best Practices

### DO:
- ✓ Run demos in a safe environment
- ✓ Review code before executing
- ✓ Use for education and training
- ✓ Test security features
- ✓ Verify source integrity first

### DON'T:
- ✗ Run attack simulations on production systems
- ✗ Modify to bypass security features
- ✗ Use for actual malicious purposes
- ✗ Disable safety limits for "better demos"

## Next Steps

After running the demos:

1. **Read the docs:** `docs/USE_CASES.md`
2. **Try examples:** `examples/` directory
3. **Deploy:** `docs/DEPLOYMENT.md`
4. **Monitor:** Set up `tools/worm_monitor.sh`

## Support

For questions or issues:
- Check `docs/QUICKSTART.md`
- Review `docs/SECURITY.md`
- See main `README.md`

---

**Remember:** All demonstrations show DEFENSIVE security capabilities. Worm Python is designed to protect systems, not attack them.
