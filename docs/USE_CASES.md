# Worm Python - Intended Use Cases

This document highlights the intended use cases for Worm Python, a security-hardened Python distribution designed for defensive security operations.

## Overview

Worm Python is designed for scenarios where **network isolation** and **security hardening** are critical requirements. It maintains full Python functionality while preventing all network access and providing additional security layers.

---

## Primary Use Cases

### 1. Executing Untrusted Code Safely

**Scenario**: Running user-submitted Python scripts where you don't fully trust the source.

**Examples**:
- Code competition platforms (HackerRank, LeetCode, etc.)
- Student homework submissions
- Bug bounty program submissions
- Automated code review systems
- CI/CD pipelines testing external contributions

**Why Worm Python**:
- ✓ Prevents data exfiltration over the network
- ✓ Blocks remote code execution attempts
- ✓ Resource limits prevent DoS attacks
- ✓ Audit logging tracks all security events
- ✓ Print-free IoC detects screen manipulation

**Example**:
```bash
# Run untrusted student submission safely
worm --strict student_submission.py < test_input.txt
```

---

### 2. Processing Sensitive Data Without Exfiltration Risk

**Scenario**: Analyzing confidential information where data must not leave the system.

**Examples**:
- Healthcare data processing (HIPAA compliance)
- Financial transaction analysis
- Personal identifiable information (PII) processing
- Classified/confidential document analysis
- Cryptocurrency wallet operations
- Legal document processing

**Why Worm Python**:
- ✓ **Zero network access** - Data cannot be sent externally
- ✓ Filesystem sandbox can restrict where data is written
- ✓ Audit logs prove no exfiltration occurred
- ✓ All computation done locally

**Example**:
```bash
# Process sensitive medical records
worm --audit --read-only process_patient_data.py records.csv
```

---

### 3. Educational Environments

**Scenario**: Teaching Python programming in schools, bootcamps, or online courses.

**Examples**:
- Computer science classrooms
- Coding bootcamps
- Online learning platforms
- Programming workshops
- Student lab environments

**Why Worm Python**:
- ✓ Students can't accidentally (or intentionally) access network
- ✓ Prevents students from cheating by downloading solutions
- ✓ Resource limits prevent one student from affecting others
- ✓ Teaches security-aware programming
- ✓ Safe environment for experimenting

**Example**:
```bash
# Student practice environment
worm --moderate repl  # Interactive REPL with moderate restrictions
```

---

### 4. Automated Testing & Continuous Integration

**Scenario**: Running automated tests on code from various sources.

**Examples**:
- CI/CD pipelines testing pull requests
- Automated testing frameworks
- Package verification before deployment
- Security scanning of dependencies
- Pre-deployment validation

**Why Worm Python**:
- ✓ Test code can't phone home to attackers
- ✓ Supply chain attack prevention
- ✓ Resource limits prevent test hangs
- ✓ Audit trail of all test runs
- ✓ Reproducible test environment

**Example**:
```bash
# Test external PR safely
worm --strict --cpu-limit 60 run_tests.py
```

---

### 5. Data Science & Analysis (Air-Gapped Environments)

**Scenario**: Data analysis in secure or air-gapped environments.

**Examples**:
- Government secure facilities
- Defense contractor analysis
- Research on confidential datasets
- Offline data processing
- Secure computation environments

**Why Worm Python**:
- ✓ Guaranteed air-gap enforcement
- ✓ Full numpy/pandas/scipy support (local computation)
- ✓ Can't accidentally connect to external APIs
- ✓ Perfect for classified networks
- ✓ Audit trail for compliance

**Example**:
```bash
# Analyze classified data
worm --audit --read-only analyze_classified_dataset.py
```

---

### 6. Malware Analysis (Behavioral Sandbox)

**Scenario**: Analyzing potentially malicious Python scripts or packages.

**Examples**:
- Security research
- Malware behavior analysis
- Suspicious package investigation
- Threat intelligence gathering
- Security incident response

**Why Worm Python**:
- ✓ Malware can't call command & control servers
- ✓ Safe detonation environment
- ✓ Network behavior analysis (all blocked)
- ✓ Audit log captures attempted malicious actions
- ✓ Print() IoC detects screen manipulation attempts

**Example**:
```bash
# Safely analyze suspicious script
worm --strict --audit --cpu-limit 30 suspicious_package.py
```

---

### 7. Code Review & Security Auditing

**Scenario**: Running code during security reviews to understand behavior.

**Examples**:
- Pre-deployment security audits
- Third-party library evaluation
- Code quality review
- Vulnerability assessment
- Compliance verification

**Why Worm Python**:
- ✓ Safe to run during review
- ✓ Behavior analysis without risk
- ✓ Identifies network dependencies
- ✓ Audit log shows what code attempted
- ✓ Restricted builtins prevent eval/exec tricks

**Example**:
```bash
# Review third-party library safely
worm --audit vendor_library_test.py
```

---

### 8. Embedded Systems & IoT Devices

**Scenario**: Python on embedded devices where network should be controlled separately.

**Examples**:
- Industrial control systems
- Medical devices
- Automotive systems
- Robotics control
- Sensor data processing

**Why Worm Python**:
- ✓ Application logic can't interfere with network layer
- ✓ Separation of concerns (network handled separately)
- ✓ Resource limits for embedded constraints
- ✓ Predictable behavior
- ✓ Security-first design

---

### 9. Competitive Programming Judging

**Scenario**: Automated judging systems for programming competitions.

**Examples**:
- ACM ICPC judging
- Online competitive programming platforms
- Hackathon automated testing
- Algorithm competition grading
- Coding interview platforms

**Why Worm Python**:
- ✓ Participants can't cheat by accessing external resources
- ✓ Resource limits ensure fair competition
- ✓ Fast, secure execution
- ✓ Prevents system manipulation
- ✓ Standardized environment

**Example**:
```bash
# Judge submission with strict limits
worm --strict --cpu-limit 5 --memory-limit 256 solution.py < input.txt
```

---

### 10. Financial Trading (Backtesting & Analysis)

**Scenario**: Running trading strategies and backtests on historical data.

**Examples**:
- Algorithmic trading backtests
- Risk analysis calculations
- Portfolio optimization
- Financial model validation
- Market data analysis

**Why Worm Python**:
- ✓ Strategy can't leak to external parties
- ✓ Prevents accidental live trading
- ✓ Pure computational analysis
- ✓ No data exfiltration risk
- ✓ Audit trail for compliance

---

## Security Profiles

Worm Python can be configured with different security profiles for different use cases:

### Strict Mode
**For**: Untrusted code, competitions, external submissions
```bash
worm --strict \
     --cpu-limit 30 \
     --memory-limit 256 \
     --no-eval \
     --read-only \
     --audit
```

### Moderate Mode (Default)
**For**: General use, data processing, analysis
```bash
worm --moderate \
     --cpu-limit 300 \
     --memory-limit 2048 \
     --audit
```

### Relaxed Mode
**For**: Trusted code, development, testing
```bash
worm --relaxed \
     --cpu-limit 3600 \
     --memory-limit 4096
```

---

## What Worm Python is NOT For

To clarify the boundaries of appropriate use:

### ✗ NOT For:
- **Standard web development** - Web apps need network access
- **API development** - APIs require network functionality
- **Microservices** - Designed for networked communication
- **Web scraping** - Requires HTTP access
- **Cloud services** - Inherently networked
- **Real-time communications** - Needs sockets
- **Production web servers** - Requires network stack

### ✓ Instead Use Standard Python For:
- Django/Flask applications
- REST API servers
- Websocket servers
- HTTP clients
- Network services
- Distributed systems

---

## Key Security Features by Use Case

| Use Case | Network Block | Resource Limits | Audit Log | Print-free IoC | Sandboxing |
|----------|--------------|-----------------|-----------|----------------|------------|
| Untrusted Code | ✓✓✓ | ✓✓✓ | ✓✓ | ✓✓ | ✓ |
| Sensitive Data | ✓✓✓ | ✓ | ✓✓✓ | ✓ | ✓✓ |
| Education | ✓✓ | ✓✓ | ✓ | ✓ | ✓ |
| CI/CD Testing | ✓✓✓ | ✓✓ | ✓✓ | ✓ | ✓ |
| Data Science | ✓✓✓ | ✓ | ✓✓ | - | ✓ |
| Malware Analysis | ✓✓✓ | ✓✓ | ✓✓✓ | ✓✓✓ | ✓✓ |
| Code Review | ✓✓ | ✓ | ✓✓✓ | ✓✓ | ✓ |
| Competitions | ✓✓✓ | ✓✓✓ | ✓ | ✓✓ | ✓ |

**Legend**: ✓✓✓ Critical | ✓✓ Important | ✓ Useful | - Not Needed

---

## Real-World Deployment Examples

### Example 1: University Computer Lab

```bash
# Install Worm Python system-wide
sudo ./scripts/install.sh

# Create wrapper for student accounts
cat > /usr/local/bin/python-student << 'EOF'
#!/bin/bash
worm --moderate --cpu-limit 180 --memory-limit 1024 "$@"
EOF
chmod +x /usr/local/bin/python-student

# Students use: python-student homework.py
```

### Example 2: Automated Code Judge

```python
# judge_service.py
import subprocess
import sys

def judge_submission(code_file, test_input):
    """Judge a submission safely."""
    result = subprocess.run(
        ['worm', '--strict', '--cpu-limit', '10',
         '--memory-limit', '128', code_file],
        input=test_input,
        capture_output=True,
        timeout=15
    )
    return result.stdout, result.stderr, result.returncode
```

### Example 3: Secure Data Processing Pipeline

```bash
#!/bin/bash
# process_sensitive_data.sh

# Enable audit logging
export WORM_AUDIT_LOG=/secure/logs/audit.log

# Process data in read-only mode
worm --read-only --audit \
     process_pii.py \
     /secure/data/input.csv \
     /secure/data/output.csv

# Verify no IoCs detected
python3 /tools/ioc_monitor.py --log-file $WORM_AUDIT_LOG
```

---

## Compliance & Regulatory Use

Worm Python supports compliance with various regulatory requirements:

- **HIPAA**: Prevents patient data exfiltration
- **GDPR**: Ensures PII stays local
- **PCI-DSS**: Protects payment data processing
- **ITAR**: Secure handling of controlled technical data
- **SOC 2**: Audit trails and access controls
- **FedRAMP**: Government security requirements

---

## Summary

Worm Python is designed for scenarios where:

1. **Network isolation is required** - Air-gapped or restricted environments
2. **Untrusted code must run** - External submissions, user scripts
3. **Data security is critical** - Confidential, sensitive, or regulated data
4. **Resource control is needed** - Prevent DoS, ensure fair allocation
5. **Audit trails are important** - Compliance, investigation, verification
6. **Security is non-negotiable** - High-risk environments

**Core Philosophy**: Provide full Python functionality for computation while eliminating network attack surface and providing defense-in-depth security layers.
