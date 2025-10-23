#!/usr/bin/env python3
"""
ARC Prize Workflow - Step 3: Evaluate Model

This script evaluates the trained solver on the ARC evaluation set.

✓ USE WORM PYTHON for this script
  No network access needed - all computation is local.

Usage:
    worm 03_evaluate.py

This will evaluate the solver and show detailed results.
"""

import sys
import os
import json
import time
from arc_solver import ARCSolver, load_task, visualize_grid


def evaluate_on_dataset():
    """Evaluate the solver on the ARC evaluation set."""
    sys.stdout.write("=" * 70 + "\n")
    sys.stdout.write("ARC Prize Workflow - Step 3: Evaluate Model\n")
    sys.stdout.write("=" * 70 + "\n\n")

    # Check if running under Worm Python
    if os.environ.get('WORM_PYTHON') == '1':
        sys.stdout.write("✓ Running under Worm Python (secure mode)\n\n")
    else:
        sys.stdout.write("⚠ Not running under Worm Python\n")
        sys.stdout.write("  Recommended: worm 03_evaluate.py\n\n")

    # Locate evaluation data
    evaluation_dir = "data/ARC-master/data/evaluation"

    if not os.path.exists(evaluation_dir):
        sys.stderr.write(f"✗ Evaluation directory not found: {evaluation_dir}\n")
        sys.stderr.write("  Run: python3 01_download_dataset.py first\n")
        sys.exit(1)

    # Get all evaluation tasks
    evaluation_files = sorted([
        f for f in os.listdir(evaluation_dir)
        if f.endswith('.json')
    ])

    sys.stdout.write(f"Found {len(evaluation_files)} evaluation tasks\n\n")

    # Initialize solver
    solver = ARCSolver()

    # Evaluation statistics
    total_accuracy = 0.0
    perfect_tasks = 0
    task_count = 0
    start_time = time.time()

    results = []

    # Evaluate on each task
    sys.stdout.write("Evaluation progress:\n")
    sys.stdout.write("-" * 70 + "\n")

    for idx, filename in enumerate(evaluation_files, 1):
        file_path = os.path.join(evaluation_dir, filename)

        # Load task
        task_data = load_task(file_path)

        # Evaluate
        accuracy = solver.evaluate(task_data)

        total_accuracy += accuracy
        task_count += 1

        if accuracy == 1.0:
            perfect_tasks += 1

        # Store result
        results.append({
            'task': filename,
            'accuracy': accuracy,
            'perfect': accuracy == 1.0
        })

        # Progress indicator
        if idx % 25 == 0 or idx == len(evaluation_files):
            avg_accuracy = (total_accuracy / task_count) * 100
            perfect_pct = (perfect_tasks / task_count) * 100
            sys.stdout.write(f"  {idx:3d}/{len(evaluation_files)} tasks")
            sys.stdout.write(f" | Avg: {avg_accuracy:.1f}%")
            sys.stdout.write(f" | Perfect: {perfect_pct:.1f}%\n")

    # Evaluation summary
    elapsed_time = time.time() - start_time
    final_accuracy = (total_accuracy / task_count) * 100
    perfect_percentage = (perfect_tasks / task_count) * 100

    sys.stdout.write("-" * 70 + "\n")
    sys.stdout.write("\nEvaluation Results:\n")
    sys.stdout.write(f"  Tasks evaluated: {task_count}\n")
    sys.stdout.write(f"  Average accuracy: {final_accuracy:.2f}%\n")
    sys.stdout.write(f"  Perfect solutions: {perfect_tasks}/{task_count} ({perfect_percentage:.1f}%)\n")
    sys.stdout.write(f"  Evaluation time: {elapsed_time:.1f} seconds\n")

    # Show some specific results
    sys.stdout.write("\n")
    sys.stdout.write("Top 5 best results:\n")
    sorted_results = sorted(results, key=lambda x: x['accuracy'], reverse=True)
    for i, result in enumerate(sorted_results[:5], 1):
        status = "✓" if result['perfect'] else "•"
        sys.stdout.write(f"  {status} {result['task']}: {result['accuracy']*100:.0f}%\n")

    sys.stdout.write("\n")
    sys.stdout.write("Bottom 5 worst results:\n")
    for i, result in enumerate(sorted_results[-5:], 1):
        status = "✗" if result['accuracy'] == 0 else "•"
        sys.stdout.write(f"  {status} {result['task']}: {result['accuracy']*100:.0f}%\n")

    # Save evaluation results
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    eval_results = {
        'tasks_evaluated': task_count,
        'average_accuracy': final_accuracy,
        'perfect_tasks': perfect_tasks,
        'perfect_percentage': perfect_percentage,
        'evaluation_time': elapsed_time,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'worm_python': os.environ.get('WORM_PYTHON') == '1',
        'detailed_results': results
    }

    results_path = os.path.join(results_dir, "evaluation_results.json")

    with open(results_path, 'w') as f:
        json.dump(eval_results, f, indent=2)

    sys.stdout.write(f"\n✓ Results saved: {results_path}\n")

    # Performance analysis
    sys.stdout.write("\n")
    sys.stdout.write("=" * 70 + "\n")
    sys.stdout.write("Evaluation Complete!\n")
    sys.stdout.write("=" * 70 + "\n\n")

    sys.stdout.write("Analysis:\n")

    if final_accuracy < 10:
        sys.stdout.write("  ⚠ Low accuracy - this simple solver needs improvement\n")
        sys.stdout.write("  Consider:\n")
        sys.stdout.write("    • Implementing more transformation types\n")
        sys.stdout.write("    • Using neural networks\n")
        sys.stdout.write("    • Applying program synthesis\n")
        sys.stdout.write("    • Adding ensemble methods\n")
    elif final_accuracy < 30:
        sys.stdout.write("  • Fair performance for a baseline solver\n")
        sys.stdout.write("  • Many ARC tasks require more sophisticated approaches\n")
    else:
        sys.stdout.write("  ✓ Good performance!\n")
        sys.stdout.write("  • Continue optimizing for better results\n")

    sys.stdout.write("\n")

    sys.stdout.write("Next steps:\n")
    sys.stdout.write("  1. Analyze failed tasks to improve solver\n")
    sys.stdout.write("  2. Generate test predictions: worm 04_generate_predictions.py\n")
    sys.stdout.write("  3. Submit to competition: python3 05_submit.py\n")
    sys.stdout.write("\n")

    # Security reminder
    if os.environ.get('WORM_PYTHON') == '1':
        sys.stdout.write("Security:\n")
        sys.stdout.write("  ✓ All evaluation performed locally\n")
        sys.stdout.write("  ✓ No network access - results cannot be leaked\n")
        sys.stdout.write("  ✓ Data protected by Worm Python\n")
        sys.stdout.write("\n")


if __name__ == '__main__':
    evaluate_on_dataset()
