# Worm Python - Production Deployment Guide

This guide covers deploying Worm Python in production environments with all security features enabled.

---

## Table of Contents

1. [Installation](#installation)
2. [Security Configuration](#security-configuration)
3. [Monitoring Setup](#monitoring-setup)
4. [Integration Examples](#integration-examples)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)

---

## Installation

### System Requirements

- **OS**: Linux (recommended), macOS, or Windows
- **Python**: 3.8 or higher
- **Disk Space**: 50MB minimum
- **Permissions**: Root/admin for system-wide installation (optional)

### Installation Steps

#### Option 1: User Installation (Recommended for Development)

```bash
cd /path/to/COMPLEXITY
./scripts/install.sh
```

This installs to `~/.local/lib/worm-python` and `~/.local/bin/worm`.

#### Option 2: System-Wide Installation (Production)

```bash
cd /path/to/COMPLEXITY
sudo ./scripts/install.sh
```

This installs to `/usr/local/lib/worm-python` and `/usr/local/bin/worm`.

#### Option 3: Custom Location

```bash
# Edit install.sh to set custom paths
export INSTALL_DIR="/opt/worm-python"
export BIN_DIR="/opt/bin"
sudo ./scripts/install.sh
```

### Verification

```bash
# Check installation
worm --version
worm --info

# Verify source integrity (NO print statements should be found)
python3 tools/ioc_monitor.py --verify-worm-source
```

---

## Security Configuration

### Configuration File

Create `/etc/worm/config.env` (system) or `~/.worm/config.env` (user):

```bash
# Worm Python Configuration

# Security Profile (strict, moderate, relaxed)
WORM_SECURITY_PROFILE=moderate

# Audit Logging
WORM_AUDIT_ENABLED=true
WORM_AUDIT_LOG=/var/log/worm/audit.log

# Resource Limits
WORM_CPU_LIMIT=300
WORM_MEMORY_LIMIT=2048
WORM_FILE_SIZE_LIMIT=100

# Restricted Builtins
WORM_RESTRICT_EVAL=true
WORM_RESTRICT_EXEC=true
WORM_RESTRICT_COMPILE=false

# Filesystem Sandbox
WORM_FS_SANDBOX=disabled
WORM_FS_ALLOWED_PATHS=/home,/tmp
WORM_FS_DENIED_PATHS=/etc,/var

# Seccomp (Linux only)
WORM_SECCOMP_ENABLED=true
```

### Security Profiles

#### Strict Profile (Untrusted Code)

```bash
export WORM_SECURITY_PROFILE=strict
export WORM_CPU_LIMIT=30
export WORM_MEMORY_LIMIT=512
export WORM_RESTRICT_EVAL=true
export WORM_RESTRICT_EXEC=true
export WORM_RESTRICT_COMPILE=true
export WORM_FS_SANDBOX=read_only
export WORM_AUDIT_ENABLED=true
```

#### Moderate Profile (General Use)

```bash
export WORM_SECURITY_PROFILE=moderate
export WORM_CPU_LIMIT=300
export WORM_MEMORY_LIMIT=2048
export WORM_RESTRICT_EVAL=true
export WORM_AUDIT_ENABLED=true
```

#### Relaxed Profile (Trusted Code)

```bash
export WORM_SECURITY_PROFILE=relaxed
export WORM_CPU_LIMIT=3600
export WORM_MEMORY_LIMIT=4096
export WORM_AUDIT_ENABLED=false
```

---

## Monitoring Setup

### 1. Audit Log Configuration

```bash
# Create log directory
sudo mkdir -p /var/log/worm
sudo chown worm-user:worm-user /var/log/worm
sudo chmod 750 /var/log/worm

# Configure log rotation
sudo cat > /etc/logrotate.d/worm << 'EOF'
/var/log/worm/audit.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 worm-user worm-user
    sharedscripts
    postrotate
        # Optional: trigger alert on rotation
        /usr/local/bin/worm_audit_check.sh
    endscript
}
EOF
```

### 2. Real-Time Monitoring Service

Create `/etc/systemd/system/worm-monitor.service`:

```ini
[Unit]
Description=Worm Python Security Monitor
After=network.target

[Service]
Type=simple
User=worm-user
ExecStart=/path/to/tools/worm_monitor.sh follow
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable worm-monitor
sudo systemctl start worm-monitor
sudo systemctl status worm-monitor
```

### 3. IoC Alert System

Create `/usr/local/bin/worm_alert.sh`:

```bash
#!/bin/bash
# Alert on IoC detection

LOG_FILE="/var/log/worm/audit.log"
ALERT_EMAIL="security@example.com"

# Check for new IoCs
if grep -q "IOC_DETECTED" "$LOG_FILE"; then
    # Extract IoC details
    iocs=$(grep "IOC_DETECTED" "$LOG_FILE" | tail -10)

    # Send alert
    echo "$iocs" | mail -s "CRITICAL: Worm Python IoC Detected" "$ALERT_EMAIL"

    # Log to syslog
    logger -t worm-security -p security.crit "IoC detected in Worm Python"

    # Optional: Trigger incident response
    # /usr/local/bin/incident_response.sh
fi
```

### 4. Monitoring Dashboard Integration

#### Prometheus Metrics (Optional)

Create custom metrics exporter for monitoring:

```python
# /usr/local/bin/worm_metrics.py
from prometheus_client import start_http_server, Gauge
import sys
sys.path.insert(0, '/usr/local/lib/worm-python')

from worm.security import read_audit_log

# Metrics
blocked_imports = Gauge('worm_blocked_imports_total', 'Total blocked imports')
blocked_subprocess = Gauge('worm_blocked_subprocess_total', 'Total blocked subprocess')
ioc_detected = Gauge('worm_ioc_detected_total', 'Total IoCs detected')

def collect_metrics():
    events = read_audit_log()
    blocked_imports.set(sum(1 for e in events if e['event_type'] == 'blocked_import'))
    blocked_subprocess.set(sum(1 for e in events if e['event_type'] == 'blocked_subprocess'))
    ioc_detected.set(sum(1 for e in events if e['event_type'] == 'IOC_DETECTED'))

if __name__ == '__main__':
    start_http_server(9100)
    while True:
        collect_metrics()
        time.sleep(60)
```

---

## Integration Examples

### 1. Web Application (Flask/Django)

```python
# app.py - Run user code safely
from flask import Flask, request
import subprocess
import tempfile
import os

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_code():
    code = request.json['code']

    # Write code to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        code_file = f.name

    try:
        # Execute with strict limits
        result = subprocess.run(
            ['worm', '--strict', '--cpu-limit', '5',
             '--memory-limit', '128', code_file],
            capture_output=True,
            timeout=10,
            text=True
        )

        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'exit_code': result.returncode
        }
    finally:
        os.unlink(code_file)
```

### 2. CI/CD Pipeline (GitHub Actions)

```.yaml
# .github/workflows/test.yml
name: Test with Worm Python

on: [pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Install Worm Python
        run: |
          git clone https://github.com/your-org/worm-python
          cd worm-python
          ./scripts/install.sh

      - name: Run tests safely
        run: |
          worm --strict --audit tests/run_all.py

      - name: Check for IoCs
        run: |
          python3 worm-python/tools/ioc_monitor.py --log-file ~/.worm/audit.log
```

### 3. Docker Container

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Install Worm Python
COPY . /tmp/worm-python
WORKDIR /tmp/worm-python
RUN ./scripts/install.sh && rm -rf /tmp/worm-python

# Create non-root user
RUN useradd -m -s /bin/bash wormuser
USER wormuser

# Set up environment
ENV WORM_SECURITY_PROFILE=strict
ENV WORM_AUDIT_ENABLED=true
ENV WORM_AUDIT_LOG=/home/wormuser/.worm/audit.log

ENTRYPOINT ["worm"]
```

### 4. Kubernetes Job

```yaml
# worm-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: worm-processing-job
spec:
  template:
    spec:
      containers:
      - name: worm
        image: your-registry/worm-python:latest
        command: ["worm"]
        args: ["--strict", "--audit", "/scripts/process_data.py"]
        resources:
          limits:
            memory: "2Gi"
            cpu: "1"
        volumeMounts:
        - name: scripts
          mountPath: /scripts
        - name: audit-logs
          mountPath: /home/wormuser/.worm
      restartPolicy: Never
      volumes:
      - name: scripts
        configMap:
          name: processing-scripts
      - name: audit-logs
        persistentVolumeClaim:
          claimName: worm-audit-logs
```

---

## Best Practices

### Security

1. **Always enable audit logging in production**
   ```bash
   export WORM_AUDIT_ENABLED=true
   ```

2. **Use strict profile for untrusted code**
   ```bash
   worm --strict untrusted_script.py
   ```

3. **Regularly check for IoCs**
   ```bash
   # Daily cron job
   0 2 * * * /usr/local/bin/worm_ioc_check.sh
   ```

4. **Verify source integrity after updates**
   ```bash
   python3 tools/ioc_monitor.py --verify-worm-source
   ```

5. **Monitor audit logs continuously**
   ```bash
   tools/worm_monitor.sh follow
   ```

### Performance

1. **Set appropriate resource limits**
   - Too strict: Legitimate code fails
   - Too relaxed: DoS risk remains

2. **Use moderate profile as baseline**
   ```bash
   export WORM_SECURITY_PROFILE=moderate
   ```

3. **Monitor resource usage**
   ```bash
   # Check what limits are being hit
   grep "resource_limit_hit" /var/log/worm/audit.log
   ```

### Operations

1. **Centralized logging**
   - Forward audit logs to SIEM (Splunk, ELK, etc.)
   - Set up alerts for IoC events

2. **Regular audits**
   - Review blocked operations weekly
   - Investigate any IoC detections immediately

3. **Backup configurations**
   - Version control security configs
   - Document any custom settings

---

## Troubleshooting

### Common Issues

#### Issue: "worm: command not found"

**Solution**:
```bash
# Add to PATH
export PATH="$HOME/.local/bin:$PATH"

# Or for system-wide
export PATH="/usr/local/bin:$PATH"
```

#### Issue: Module import fails

**Solution**:
```bash
# Check if module is blocked
python3 -c "from worm.hooks.import_restrictions import BLOCKED_MODULES; print(BLOCKED_MODULES)"

# If needed, use standard Python for network operations
python3 network_script.py  # NOT worm
```

#### Issue: Resource limit too restrictive

**Solution**:
```bash
# Increase limits for specific script
worm --cpu-limit 600 --memory-limit 4096 script.py

# Or modify profile
export WORM_CPU_LIMIT=600
```

#### Issue: Audit log growing too large

**Solution**:
```bash
# Set up log rotation (see Monitoring Setup section)

# Or manually rotate
sudo logrotate -f /etc/logrotate.d/worm
```

#### Issue: Seccomp not working

**Solution**:
```bash
# Check if running on Linux
uname -s

# Check if seccomp is available
python3 -c "from worm.seccomp import is_seccomp_available; print(is_seccomp_available())"

# Seccomp doesn't work in some Docker containers
# This is expected - Python-level restrictions still apply
```

### Getting Help

1. **Check logs**:
   ```bash
   # Audit log
   tail -100 ~/.worm/audit.log

   # System log (if using systemd)
   journalctl -u worm-monitor -n 100
   ```

2. **Verify integrity**:
   ```bash
   tools/ioc_monitor.py --verify-worm-source
   ```

3. **Test configuration**:
   ```bash
   # Test with simple script
   worm -c "import sys; sys.stdout.write('Test OK\n')"
   ```

---

## Maintenance

### Regular Tasks

**Daily**:
- Monitor audit logs for IoCs
- Check system resource usage

**Weekly**:
- Review blocked operations
- Analyze security events
- Rotate logs

**Monthly**:
- Update Worm Python to latest version
- Review and update security policies
- Audit user access and permissions

**Quarterly**:
- Security audit of entire deployment
- Review and update documentation
- Disaster recovery testing

---

## Compliance Documentation

For regulatory compliance, maintain:

1. **Audit Trail**: All `~/.worm/audit.log` entries
2. **Configuration Records**: Security profiles used
3. **Access Logs**: Who ran what scripts
4. **IoC Reports**: Any security incidents detected
5. **Version History**: Worm Python versions deployed

Store securely for required retention period (typically 7 years for HIPAA, etc.).

---

## Summary

Production deployment checklist:

- [ ] Install Worm Python (user or system-wide)
- [ ] Configure security profile
- [ ] Enable audit logging
- [ ] Set resource limits
- [ ] Configure log rotation
- [ ] Set up monitoring
- [ ] Configure IoC alerts
- [ ] Test with sample scripts
- [ ] Verify source integrity
- [ ] Document configuration
- [ ] Train operations team
- [ ] Establish incident response procedures

**Worm Python is now ready for production use!**
