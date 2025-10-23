#!/usr/bin/env python3
"""
Worm Python LITE - Kaggle/Competition Mode

A modified version of Worm Python designed for data science competitions.

KEY DIFFERENCES FROM STANDARD WORM PYTHON:
- Allows HTTPS to specific whitelisted domains (kaggle.com, huggingface.co)
- Blocks all other network access
- Allows downloading datasets and models
- Allows submitting competition results
- Still blocks malicious network operations

USE CASE:
- Kaggle competitions
- ARC Prize
- Other ML competitions
- Downloading datasets
- Submitting solutions
- Using pre-trained models

SECURITY:
- Blocks exfiltration to unknown domains
- Allows only competition-related network access
- Maintains resource limits
- Full audit logging
- Print-free codebase IoC detection
"""

import sys
import os

# Whitelisted domains for ML competitions
ALLOWED_DOMAINS = {
    'kaggle.com',
    'www.kaggle.com',
    'huggingface.co',
    'pytorch.org',
    'tensorflow.org',
    'github.com',  # For downloading models
    'raw.githubusercontent.com',
    'arcprize.org',
    'www.arcprize.org',
}

# Blocked domains (known malicious)
BLOCKED_DOMAINS = {
    'attacker.com',
    'evil.com',
    # Add known malicious domains
}

def is_domain_allowed(url):
    """Check if a URL's domain is in the whitelist."""
    from urllib.parse import urlparse

    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        # Remove port if present
        domain = domain.split(':')[0]

        # Check if blocked
        if domain in BLOCKED_DOMAINS:
            return False

        # Check if whitelisted
        for allowed in ALLOWED_DOMAINS:
            if domain == allowed or domain.endswith('.' + allowed):
                return True

        return False
    except:
        return False


def setup_kaggle_mode():
    """
    Set up Worm Python in Kaggle competition mode.

    This allows network access to whitelisted domains only.
    """
    sys.stdout.write("Worm Python - Kaggle Competition Mode\n")
    sys.stdout.write("Network access: Limited to whitelisted domains\n")
    sys.stdout.write(f"Allowed domains: {', '.join(sorted(ALLOWED_DOMAINS))}\n")
    sys.stdout.write("\n")

    # TODO: Implement selective network blocking
    # For now, this is a design document

    sys.stdout.write("⚠ NOTE: This is a concept/design document.\n")
    sys.stdout.write("Full implementation would require:\n")
    sys.stdout.write("  1. Modified socket module with domain filtering\n")
    sys.stdout.write("  2. urllib/requests wrapper with whitelist checking\n")
    sys.stdout.write("  3. DNS resolver with domain validation\n")
    sys.stdout.write("  4. Audit logging of all network requests\n")
    sys.stdout.write("\n")


if __name__ == '__main__':
    sys.stdout.write("═" * 70 + "\n")
    sys.stdout.write("WORM PYTHON LITE - KAGGLE/COMPETITION MODE (CONCEPT)\n")
    sys.stdout.write("═" * 70 + "\n\n")

    setup_kaggle_mode()

    sys.stdout.write("Example Usage:\n")
    sys.stdout.write("  worm-lite train.py              # Run with whitelist\n")
    sys.stdout.write("  worm-lite --submit solution.py  # Submit to Kaggle\n")
    sys.stdout.write("  worm-lite --download dataset    # Download data\n")
    sys.stdout.write("\n")

    sys.stdout.write("Security Features Maintained:\n")
    sys.stdout.write("  ✓ Resource limits (CPU, memory)\n")
    sys.stdout.write("  ✓ Audit logging\n")
    sys.stdout.write("  ✓ Print-free IoC detection\n")
    sys.stdout.write("  ✓ Restricted builtins\n")
    sys.stdout.write("  ✓ Filesystem sandbox\n")
    sys.stdout.write("  ✓ Block exfiltration to non-whitelisted domains\n")
    sys.stdout.write("\n")

    sys.stdout.write("Additional Features for Competitions:\n")
    sys.stdout.write("  ✓ Allow Kaggle API access\n")
    sys.stdout.write("  ✓ Allow downloading datasets\n")
    sys.stdout.write("  ✓ Allow submitting solutions\n")
    sys.stdout.write("  ✓ Allow downloading pre-trained models\n")
    sys.stdout.write("  ✗ Block exfiltration to unknown servers\n")
    sys.stdout.write("  ✗ Block malicious network activity\n")
    sys.stdout.write("\n")
