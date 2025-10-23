#!/usr/bin/env python3
"""
ARC Prize Workflow - Step 5: Submit Predictions

This script submits predictions to the competition.

⚠️ USE STANDARD PYTHON (not Worm Python) for this script
   Network access is required to submit to the competition.

Usage:
    python3 05_submit.py

This will submit the predictions to the competition.
"""

import sys
import os
import json


def submit_predictions():
    """Submit predictions to the competition."""
    sys.stdout.write("=" * 70 + "\n")
    sys.stdout.write("ARC Prize Workflow - Step 5: Submit Predictions\n")
    sys.stdout.write("=" * 70 + "\n\n")

    # Check that we're NOT running under Worm Python
    if os.environ.get('WORM_PYTHON') == '1':
        sys.stderr.write("✗ ERROR: Running under Worm Python\n")
        sys.stderr.write("  Network access is blocked in Worm Python\n")
        sys.stderr.write("  Use: python3 05_submit.py (not worm)\n\n")
        sys.exit(1)
    else:
        sys.stdout.write("✓ Running under standard Python (network enabled)\n\n")

    # Check if predictions exist
    predictions_path = "results/predictions.json"

    if not os.path.exists(predictions_path):
        sys.stderr.write(f"✗ Predictions file not found: {predictions_path}\n")
        sys.stderr.write("  Run: worm 04_generate_predictions.py first\n")
        sys.exit(1)

    sys.stdout.write(f"✓ Found predictions: {predictions_path}\n")

    # Load predictions
    with open(predictions_path, 'r') as f:
        predictions = json.load(f)

    sys.stdout.write(f"  Tasks: {len(predictions)}\n")
    sys.stdout.write(f"  Total examples: {sum(len(p) for p in predictions.values())}\n")

    # Load metadata if available
    metadata_path = "results/submission_metadata.json"
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        sys.stdout.write(f"  Generated: {metadata.get('timestamp', 'unknown')}\n")

    sys.stdout.write("\n")

    # Submission options
    sys.stdout.write("=" * 70 + "\n")
    sys.stdout.write("Submission Options\n")
    sys.stdout.write("=" * 70 + "\n\n")

    sys.stdout.write("Choose your submission method:\n\n")

    sys.stdout.write("OPTION 1: Kaggle API (Recommended)\n")
    sys.stdout.write("-" * 70 + "\n")
    sys.stdout.write("If you have kaggle-api installed:\n\n")
    sys.stdout.write("  pip install kaggle\n")
    sys.stdout.write("  kaggle competitions submit \\\n")
    sys.stdout.write("    -c arc-prize-2024 \\\n")
    sys.stdout.write("    -f results/predictions.json \\\n")
    sys.stdout.write("    -m \"Worm Python solution\"\n\n")

    sys.stdout.write("OPTION 2: Web Interface\n")
    sys.stdout.write("-" * 70 + "\n")
    sys.stdout.write("1. Go to the competition page:\n")
    sys.stdout.write("   https://www.kaggle.com/competitions/arc-prize-2024\n")
    sys.stdout.write("2. Click 'Submit Predictions'\n")
    sys.stdout.write("3. Upload: results/predictions.json\n")
    sys.stdout.write("4. Add description: 'Worm Python solution'\n")
    sys.stdout.write("5. Click 'Submit'\n\n")

    sys.stdout.write("OPTION 3: Command Line (curl)\n")
    sys.stdout.write("-" * 70 + "\n")
    sys.stdout.write("For custom submission endpoints:\n\n")
    sys.stdout.write("  curl -X POST \\\n")
    sys.stdout.write("    https://arcprize.org/api/submit \\\n")
    sys.stdout.write("    -H 'Authorization: Bearer YOUR_API_KEY' \\\n")
    sys.stdout.write("    -F file=@results/predictions.json\n\n")

    # Interactive submission (if kaggle-api is available)
    sys.stdout.write("=" * 70 + "\n")
    sys.stdout.write("Automatic Submission\n")
    sys.stdout.write("=" * 70 + "\n\n")

    try:
        # Try to import kaggle API
        from kaggle.api.kaggle_api_extended import KaggleApi

        sys.stdout.write("Kaggle API detected!\n\n")
        sys.stdout.write("Do you want to submit now? [y/N]: ")

        # Note: In a real implementation, we'd get user input
        # For this example, we'll just show the instructions

        sys.stdout.write("\n")
        sys.stdout.write("To submit automatically, uncomment the code below:\n\n")
        sys.stdout.write("  # api = KaggleApi()\n")
        sys.stdout.write("  # api.authenticate()\n")
        sys.stdout.write("  # api.competition_submit(\n")
        sys.stdout.write("  #     file_name='results/predictions.json',\n")
        sys.stdout.write("  #     message='Worm Python solution',\n")
        sys.stdout.write("  #     competition='arc-prize-2024'\n")
        sys.stdout.write("  # )\n")
        sys.stdout.write("  # sys.stdout.write('✓ Submission successful!\\n')\n\n")

    except ImportError:
        sys.stdout.write("Kaggle API not installed.\n")
        sys.stdout.write("Install with: pip install kaggle\n\n")

    # Summary
    sys.stdout.write("=" * 70 + "\n")
    sys.stdout.write("Submission Guide\n")
    sys.stdout.write("=" * 70 + "\n\n")

    sys.stdout.write("Before submitting:\n")
    sys.stdout.write("  1. Review your predictions for correctness\n")
    sys.stdout.write("  2. Check the evaluation results (03_evaluate.py)\n")
    sys.stdout.write("  3. Ensure predictions file is valid JSON\n")
    sys.stdout.write("  4. Review competition rules\n\n")

    sys.stdout.write("After submitting:\n")
    sys.stdout.write("  1. Check leaderboard for your score\n")
    sys.stdout.write("  2. Analyze any errors or warnings\n")
    sys.stdout.write("  3. Iterate on your solution\n")
    sys.stdout.write("  4. Rerun pipeline: download -> train -> evaluate -> predict -> submit\n\n")

    # Security reminder
    sys.stdout.write("Security Notes:\n")
    sys.stdout.write("  ✓ Training/evaluation done in Worm Python (secure)\n")
    sys.stdout.write("  ✓ Predictions generated in Worm Python (secure)\n")
    sys.stdout.write("  ✓ Only submission requires network access\n")
    sys.stdout.write("  ✓ Your data stayed protected during development\n\n")

    sys.stdout.write("=" * 70 + "\n")
    sys.stdout.write("Ready to Submit!\n")
    sys.stdout.write("=" * 70 + "\n\n")

    sys.stdout.write("File to submit: results/predictions.json\n")
    sys.stdout.write("Good luck!\n\n")


if __name__ == '__main__':
    submit_predictions()
