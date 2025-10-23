#!/usr/bin/env python3
"""
Simple ARC Solver - Worm Python Compatible

A basic heuristic-based solver for ARC tasks that demonstrates the hybrid
workflow approach. This solver uses only allowed libraries (numpy) and
performs all computation locally without any network access.

This is a simplified example. Real ARC solutions would use more sophisticated
approaches (neural networks, program synthesis, etc.).
"""

import sys
import json
import numpy as np


class ARCSolver:
    """
    Simple ARC task solver using basic heuristics.

    This solver tries several simple transformations:
    1. Copy input (identity)
    2. Transpose
    3. Horizontal flip
    4. Vertical flip
    5. Color mapping (most common color)
    6. Size scaling
    """

    def __init__(self):
        self.trained_patterns = {}

    def train(self, task_data):
        """
        Learn patterns from training examples.

        Args:
            task_data: Dictionary with 'train' key containing examples
        """
        task_id = id(task_data)  # Simple ID for this task
        patterns = []

        for example in task_data.get('train', []):
            input_grid = np.array(example['input'])
            output_grid = np.array(example['output'])

            # Analyze transformation
            pattern = self._analyze_transformation(input_grid, output_grid)
            patterns.append(pattern)

        self.trained_patterns[task_id] = patterns
        return task_id

    def _analyze_transformation(self, input_grid, output_grid):
        """Analyze what transformation was applied."""
        pattern = {
            'input_shape': input_grid.shape,
            'output_shape': output_grid.shape,
            'transformation': 'unknown'
        }

        # Check if it's identity (copy)
        if np.array_equal(input_grid, output_grid):
            pattern['transformation'] = 'identity'

        # Check if it's transpose
        elif input_grid.shape == output_grid.shape[::-1]:
            if np.array_equal(input_grid.T, output_grid):
                pattern['transformation'] = 'transpose'

        # Check if it's horizontal flip
        elif np.array_equal(np.fliplr(input_grid), output_grid):
            pattern['transformation'] = 'flip_horizontal'

        # Check if it's vertical flip
        elif np.array_equal(np.flipud(input_grid), output_grid):
            pattern['transformation'] = 'flip_vertical'

        # Check if shapes are different (scaling)
        elif input_grid.shape != output_grid.shape:
            pattern['transformation'] = 'scale'
            pattern['scale_factor'] = (
                output_grid.shape[0] / input_grid.shape[0],
                output_grid.shape[1] / input_grid.shape[1]
            )

        return pattern

    def predict(self, task_id, test_input):
        """
        Generate prediction for test input.

        Args:
            task_id: ID of the trained task
            test_input: Input grid to transform

        Returns:
            Predicted output grid
        """
        if task_id not in self.trained_patterns:
            # No training data, return input as-is
            return test_input

        patterns = self.trained_patterns[task_id]

        # Use the most common transformation
        transformations = [p['transformation'] for p in patterns]
        most_common = max(set(transformations), key=transformations.count)

        input_grid = np.array(test_input)

        # Apply the transformation
        if most_common == 'identity':
            return input_grid.tolist()

        elif most_common == 'transpose':
            return input_grid.T.tolist()

        elif most_common == 'flip_horizontal':
            return np.fliplr(input_grid).tolist()

        elif most_common == 'flip_vertical':
            return np.flipud(input_grid).tolist()

        elif most_common == 'scale':
            # For scaling, use the first pattern's scale factor
            scale_pattern = [p for p in patterns if p['transformation'] == 'scale'][0]
            scale_factor = scale_pattern.get('scale_factor', (1, 1))

            new_shape = (
                int(input_grid.shape[0] * scale_factor[0]),
                int(input_grid.shape[1] * scale_factor[1])
            )

            # Simple nearest-neighbor scaling
            output_grid = np.zeros(new_shape, dtype=int)
            for i in range(new_shape[0]):
                for j in range(new_shape[1]):
                    src_i = int(i / scale_factor[0])
                    src_j = int(j / scale_factor[1])
                    output_grid[i, j] = input_grid[src_i, src_j]

            return output_grid.tolist()

        else:
            # Unknown transformation, return input
            return input_grid.tolist()

    def evaluate(self, task_data):
        """
        Evaluate solver on a task.

        Args:
            task_data: Task dictionary with 'train' and 'test' examples

        Returns:
            Accuracy (0.0 to 1.0)
        """
        # Train on this task
        task_id = self.train(task_data)

        # Test on test examples
        correct = 0
        total = 0

        for test_example in task_data.get('test', []):
            test_input = test_example['input']
            expected_output = test_example['output']

            prediction = self.predict(task_id, test_input)

            if np.array_equal(prediction, expected_output):
                correct += 1

            total += 1

        accuracy = correct / total if total > 0 else 0.0
        return accuracy


def load_task(file_path):
    """Load an ARC task from JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)


def save_predictions(predictions, output_path):
    """Save predictions to JSON file."""
    with open(output_path, 'w') as f:
        json.dump(predictions, f, indent=2)


def visualize_grid(grid, label="Grid"):
    """
    Simple ASCII visualization of a grid.

    Uses characters to represent different colors.
    """
    sys.stdout.write(f"\n{label}:\n")

    # Color mapping for visualization
    color_chars = {
        0: '.',  # Background
        1: '#',
        2: '@',
        3: '*',
        4: '+',
        5: '=',
        6: '%',
        7: '&',
        8: '$',
        9: '!',
    }

    for row in grid:
        line = ' '.join(color_chars.get(cell, '?') for cell in row)
        sys.stdout.write(line + '\n')

    sys.stdout.write('\n')


if __name__ == '__main__':
    # Simple test
    sys.stdout.write("ARC Solver Module - Worm Python Compatible\n")
    sys.stdout.write("=" * 50 + "\n\n")

    # Create a simple test case
    test_task = {
        'train': [
            {
                'input': [[1, 2], [3, 4]],
                'output': [[1, 3], [2, 4]]  # Transpose
            },
            {
                'input': [[5, 6], [7, 8]],
                'output': [[5, 7], [6, 8]]  # Transpose
            }
        ],
        'test': [
            {
                'input': [[9, 0], [1, 2]],
                'output': [[9, 1], [0, 2]]  # Expected: transpose
            }
        ]
    }

    solver = ARCSolver()

    sys.stdout.write("Training solver...\n")
    task_id = solver.train(test_task)

    sys.stdout.write("Testing prediction...\n")
    test_input = test_task['test'][0]['input']
    prediction = solver.predict(task_id, test_input)

    visualize_grid(test_input, "Input")
    visualize_grid(prediction, "Predicted Output")
    visualize_grid(test_task['test'][0]['output'], "Expected Output")

    accuracy = solver.evaluate(test_task)
    sys.stdout.write(f"Accuracy: {accuracy * 100:.1f}%\n")

    if accuracy == 1.0:
        sys.stdout.write("✓ Test passed!\n")
    else:
        sys.stdout.write("✗ Test failed\n")
