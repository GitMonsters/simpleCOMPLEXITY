#!/usr/bin/env python3
"""
ARC Prize Workflow - Step 4: Generate Predictions

This script generates predictions for the test set and saves them in the
format required for competition submission.

✓ USE WORM PYTHON for this script
  No network access needed - all computation is local.

Usage:
    worm 04_generate_predictions.py

This will generate predictions.json ready for submission.
"""

import sys
import os
import json
import time
from arc_solver import ARCSolver, load_task


def generate_predictions():
    """Generate predictions for the test set."""
    sys.stdout.write("=" * 70 + "\n")
    sys.stdout.write("ARC Prize Workflow - Step 4: Generate Predictions\n")
    sys.stdout.write("=" * 70 + "\n\n")

    # Check if running under Worm Python
    if os.environ.get('WORM_PYTHON') == '1':
        sys.stdout.write("✓ Running under Worm Python (secure mode)\n\n")
    else:
        sys.stdout.write("⚠ Not running under Worm Python\n")
        sys.stdout.write("  Recommended: worm 04_generate_predictions.py\n\n")

    # Locate test data
    # Note: Real ARC Prize test data might be in a different location
    # For this example, we'll use the evaluation set as "test"
    test_dir = "data/ARC-master/data/evaluation"

    if not os.path.exists(test_dir):
        sys.stderr.write(f"✗ Test directory not found: {test_dir}\n")
        sys.stderr.write("  Run: python3 01_download_dataset.py first\n")
        sys.stderr.write("\n  Note: Using evaluation set as test set for this demo\n")
        sys.exit(1)

    # Get all test tasks
    test_files = sorted([
        f for f in os.listdir(test_dir)
        if f.endswith('.json')
    ])

    sys.stdout.write(f"Found {len(test_files)} test tasks\n\n")

    # Initialize solver
    solver = ARCSolver()

    # Predictions dictionary
    predictions = {}

    # Generate predictions
    sys.stdout.write("Generating predictions:\n")
    sys.stdout.write("-" * 70 + "\n")

    start_time = time.time()

    for idx, filename in enumerate(test_files, 1):
        file_path = os.path.join(test_dir, filename)

        # Load task
        task_data = load_task(file_path)

        # Train on this task's training examples
        task_id = solver.train(task_data)

        # Generate predictions for each test example
        task_predictions = []

        for test_example in task_data.get('test', []):
            test_input = test_example['input']

            # Generate prediction
            prediction = solver.predict(task_id, test_input)

            task_predictions.append({
                'input': test_input,
                'prediction': prediction
            })

        # Store predictions (use filename without .json as task ID)
        task_name = filename.replace('.json', '')
        predictions[task_name] = task_predictions

        # Progress indicator
        if idx % 25 == 0 or idx == len(test_files):
            sys.stdout.write(f"  {idx:3d}/{len(test_files)} tasks processed\n")

    # Summary
    elapsed_time = time.time() - start_time

    sys.stdout.write("-" * 70 + "\n")
    sys.stdout.write("\nPrediction Generation Summary:\n")
    sys.stdout.write(f"  Tasks processed: {len(predictions)}\n")
    sys.stdout.write(f"  Total test examples: {sum(len(p) for p in predictions.values())}\n")
    sys.stdout.write(f"  Processing time: {elapsed_time:.1f} seconds\n")

    # Save predictions
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    predictions_path = os.path.join(results_dir, "predictions.json")

    with open(predictions_path, 'w') as f:
        json.dump(predictions, f, indent=2)

    sys.stdout.write(f"\n✓ Predictions saved: {predictions_path}\n")

    # File size
    file_size = os.path.getsize(predictions_path)
    sys.stdout.write(f"  File size: {file_size:,} bytes ({file_size/1024:.1f} KB)\n")

    # Show example prediction
    sys.stdout.write("\n")
    sys.stdout.write("Example prediction:\n")
    sys.stdout.write("-" * 70 + "\n")

    first_task = list(predictions.keys())[0]
    first_pred = predictions[first_task][0]

    sys.stdout.write(f"Task: {first_task}\n")
    sys.stdout.write(f"Input shape: {len(first_pred['input'])}x{len(first_pred['input'][0])}\n")
    sys.stdout.write(f"Output shape: {len(first_pred['prediction'])}x{len(first_pred['prediction'][0])}\n")

    # Create submission metadata
    submission_metadata = {
        'tasks': len(predictions),
        'total_examples': sum(len(p) for p in predictions.values()),
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'worm_python': os.environ.get('WORM_PYTHON') == '1',
        'solver': 'Simple Heuristic Solver v1.0',
        'predictions_file': predictions_path
    }

    metadata_path = os.path.join(results_dir, "submission_metadata.json")

    with open(metadata_path, 'w') as f:
        json.dump(submission_metadata, f, indent=2)

    sys.stdout.write(f"\n✓ Metadata saved: {metadata_path}\n")

    # Final instructions
    sys.stdout.write("\n")
    sys.stdout.write("=" * 70 + "\n")
    sys.stdout.write("Predictions Ready for Submission!\n")
    sys.stdout.write("=" * 70 + "\n\n")

    sys.stdout.write("Files created:\n")
    sys.stdout.write(f"  • {predictions_path}\n")
    sys.stdout.write(f"  • {metadata_path}\n")
    sys.stdout.write("\n")

    sys.stdout.write("Next steps:\n")
    sys.stdout.write("  1. Review predictions: cat results/predictions.json | head\n")
    sys.stdout.write("  2. Submit to competition: python3 05_submit.py\n")
    sys.stdout.write("\n")

    sys.stdout.write("Submission options:\n")
    sys.stdout.write("  • Use Kaggle API: kaggle competitions submit\n")
    sys.stdout.write("  • Use web interface: Upload predictions.json\n")
    sys.stdout.write("  • Use curl: See 05_submit.py for example\n")
    sys.stdout.write("\n")

    # Security reminder
    if os.environ.get('WORM_PYTHON') == '1':
        sys.stdout.write("Security:\n")
        sys.stdout.write("  ✓ All predictions generated locally\n")
        sys.stdout.write("  ✓ No network access during generation\n")
        sys.stdout.write("  ✓ Predictions file ready for manual submission\n")
        sys.stdout.write("  ⚠ Use standard Python for submission (05_submit.py)\n")
        sys.stdout.write("\n")


if __name__ == '__main__':
    generate_predictions()
