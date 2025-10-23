#!/usr/bin/env python3
"""
ARC Prize Workflow - Step 2: Train Model

This script trains an ARC solver on the training dataset.

✓ USE WORM PYTHON for this script
  No network access needed - all computation is local.

Usage:
    worm 02_train_model.py

This will train the solver on the ARC training set and save the model.
"""

import sys
import os
import json
import time
from arc_solver import ARCSolver, load_task


def train_on_dataset():
    """Train the solver on the full ARC training set."""
    sys.stdout.write("=" * 70 + "\n")
    sys.stdout.write("ARC Prize Workflow - Step 2: Train Model\n")
    sys.stdout.write("=" * 70 + "\n\n")

    # Check if running under Worm Python
    if os.environ.get('WORM_PYTHON') == '1':
        sys.stdout.write("✓ Running under Worm Python (secure mode)\n\n")
    else:
        sys.stdout.write("⚠ Not running under Worm Python\n")
        sys.stdout.write("  Recommended: worm 02_train_model.py\n\n")

    # Locate training data
    training_dir = "data/ARC-master/data/training"

    if not os.path.exists(training_dir):
        sys.stderr.write(f"✗ Training directory not found: {training_dir}\n")
        sys.stderr.write("  Run: python3 01_download_dataset.py first\n")
        sys.exit(1)

    # Get all training tasks
    training_files = sorted([
        f for f in os.listdir(training_dir)
        if f.endswith('.json')
    ])

    sys.stdout.write(f"Found {len(training_files)} training tasks\n\n")

    # Initialize solver
    solver = ARCSolver()

    # Training statistics
    total_accuracy = 0.0
    task_count = 0
    start_time = time.time()

    # Train on each task
    sys.stdout.write("Training progress:\n")
    sys.stdout.write("-" * 70 + "\n")

    for idx, filename in enumerate(training_files, 1):
        file_path = os.path.join(training_dir, filename)

        # Load task
        task_data = load_task(file_path)

        # Evaluate (which includes training)
        accuracy = solver.evaluate(task_data)

        total_accuracy += accuracy
        task_count += 1

        # Progress indicator
        if idx % 50 == 0 or idx == len(training_files):
            avg_accuracy = (total_accuracy / task_count) * 100
            sys.stdout.write(f"  {idx:3d}/{len(training_files)} tasks")
            sys.stdout.write(f" | Avg accuracy: {avg_accuracy:.1f}%\n")

    # Training summary
    elapsed_time = time.time() - start_time
    final_accuracy = (total_accuracy / task_count) * 100

    sys.stdout.write("-" * 70 + "\n")
    sys.stdout.write("\nTraining Summary:\n")
    sys.stdout.write(f"  Tasks trained: {task_count}\n")
    sys.stdout.write(f"  Average accuracy: {final_accuracy:.2f}%\n")
    sys.stdout.write(f"  Training time: {elapsed_time:.1f} seconds\n")
    sys.stdout.write(f"  Tasks per second: {task_count / elapsed_time:.1f}\n")

    # Save model (in this simple case, just save stats)
    model_dir = "models"
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    model_info = {
        'training_tasks': task_count,
        'average_accuracy': final_accuracy,
        'training_time': elapsed_time,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'worm_python': os.environ.get('WORM_PYTHON') == '1',
    }

    model_info_path = os.path.join(model_dir, "model_info.json")

    with open(model_info_path, 'w') as f:
        json.dump(model_info, f, indent=2)

    sys.stdout.write(f"\n✓ Model info saved: {model_info_path}\n")

    # Performance notes
    sys.stdout.write("\n")
    sys.stdout.write("=" * 70 + "\n")
    sys.stdout.write("Training Complete!\n")
    sys.stdout.write("=" * 70 + "\n\n")

    sys.stdout.write("Notes:\n")
    sys.stdout.write("  • This is a simple baseline solver\n")
    sys.stdout.write("  • Real ARC solutions require more sophisticated approaches\n")
    sys.stdout.write("  • Consider: neural networks, program synthesis, search algorithms\n")
    sys.stdout.write("\n")

    sys.stdout.write("Next steps:\n")
    sys.stdout.write("  1. Evaluate on evaluation set: worm 03_evaluate.py\n")
    sys.stdout.write("  2. Generate predictions: worm 04_generate_predictions.py\n")
    sys.stdout.write("  3. Submit results: python3 05_submit.py\n")
    sys.stdout.write("\n")

    # Security reminder
    if os.environ.get('WORM_PYTHON') == '1':
        sys.stdout.write("Security:\n")
        sys.stdout.write("  ✓ Network access blocked - no data exfiltration possible\n")
        sys.stdout.write("  ✓ Training data protected by Worm Python\n")
        sys.stdout.write("  ✓ All computation performed locally\n")
        sys.stdout.write("\n")


if __name__ == '__main__':
    train_on_dataset()
