#!/usr/bin/env worm
"""
Example: Data Analysis with Worm Python

This script demonstrates how Worm Python can safely process data
without any risk of network exfiltration.
"""

import json
import statistics
from collections import Counter


def analyze_numbers(numbers):
    """Analyze a list of numbers."""
    return {
        'count': len(numbers),
        'sum': sum(numbers),
        'mean': statistics.mean(numbers),
        'median': statistics.median(numbers),
        'stdev': statistics.stdev(numbers) if len(numbers) > 1 else 0,
        'min': min(numbers),
        'max': max(numbers),
    }


def main():
    # Sample data
    data = [
        {'category': 'A', 'value': 10},
        {'category': 'B', 'value': 20},
        {'category': 'A', 'value': 15},
        {'category': 'C', 'value': 30},
        {'category': 'B', 'value': 25},
        {'category': 'A', 'value': 12},
    ]

    print("=== Data Analysis with Worm Python ===\n")

    # Count by category
    category_counts = Counter(item['category'] for item in data)
    print("Category counts:")
    print(json.dumps(dict(category_counts), indent=2))
    print()

    # Analyze values
    values = [item['value'] for item in data]
    stats = analyze_numbers(values)
    print("Value statistics:")
    print(json.dumps(stats, indent=2))
    print()

    # Group by category
    by_category = {}
    for item in data:
        cat = item['category']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(item['value'])

    print("Analysis by category:")
    for category, values in sorted(by_category.items()):
        cat_stats = analyze_numbers(values)
        print(f"\n{category}:")
        print(f"  Count: {cat_stats['count']}")
        print(f"  Mean: {cat_stats['mean']:.2f}")
        print(f"  Sum: {cat_stats['sum']}")

    print("\n✓ Analysis complete - No network access needed or used!")


if __name__ == '__main__':
    main()
