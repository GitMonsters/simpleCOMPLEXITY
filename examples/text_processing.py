#!/usr/bin/env worm
"""
Example: Secure Text Processing with Worm Python

This demonstrates safe text processing without network risks.
Perfect for processing sensitive documents, logs, or user-submitted content.
"""

import re
import os
from collections import defaultdict


def analyze_text(text):
    """Analyze text and return statistics."""
    # Basic stats
    lines = text.splitlines()
    words = text.split()
    chars = len(text)

    # Word frequency
    word_freq = defaultdict(int)
    for word in words:
        # Clean word
        clean_word = re.sub(r'[^\w]', '', word.lower())
        if clean_word:
            word_freq[clean_word] += 1

    # Find common words
    common_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        'lines': len(lines),
        'words': len(words),
        'chars': chars,
        'unique_words': len(word_freq),
        'common_words': common_words,
    }


def redact_sensitive_info(text):
    """Redact emails and phone numbers from text."""
    # Redact emails
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                  '[EMAIL REDACTED]', text)

    # Redact phone numbers (simple pattern)
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
                  '[PHONE REDACTED]', text)

    # Redact credit card-like numbers
    text = re.sub(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
                  '[CARD REDACTED]', text)

    return text


def main():
    print("=== Secure Text Processing with Worm Python ===\n")

    # Sample text with sensitive information
    sample_text = """
    Dear Customer,

    Thank you for your order. Your confirmation number is #12345.
    If you have questions, contact us at support@example.com or
    call 555-123-4567.

    Your payment method ending in 4532 has been charged.

    Best regards,
    The Support Team
    """

    print("Original text stats:")
    stats = analyze_text(sample_text)
    print(f"  Lines: {stats['lines']}")
    print(f"  Words: {stats['words']}")
    print(f"  Characters: {stats['chars']}")
    print(f"  Unique words: {stats['unique_words']}")
    print()

    print("Top 10 most common words:")
    for word, count in stats['common_words']:
        print(f"  {word}: {count}")
    print()

    print("Text with sensitive information redacted:")
    print("-" * 60)
    redacted = redact_sensitive_info(sample_text)
    print(redacted)
    print("-" * 60)
    print()

    # Demonstrate Worm Python environment check
    if os.environ.get('WORM_PYTHON') == '1':
        print("✓ Running in Worm Python - Sensitive data is safe from network exfiltration!")
    else:
        print("⚠ Not running in Worm Python - Use 'worm' command for maximum security")


if __name__ == '__main__':
    main()
