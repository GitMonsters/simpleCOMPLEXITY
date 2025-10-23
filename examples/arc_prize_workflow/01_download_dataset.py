#!/usr/bin/env python3
"""
ARC Prize Workflow - Step 1: Download Dataset

This script downloads the ARC (Abstraction and Reasoning Corpus) dataset
from the official GitHub repository.

⚠️ USE STANDARD PYTHON (not Worm Python) for this script
   Network access is required to download the dataset.

Usage:
    python3 01_download_dataset.py

This will create a 'data/' directory with the ARC dataset.
"""

import urllib.request
import zipfile
import os
import sys
import json

# ARC dataset URL
ARC_DATASET_URL = "https://github.com/fchollet/ARC/archive/refs/heads/master.zip"
DATA_DIR = "data"
ZIP_FILE = "ARC-master.zip"


def download_dataset():
    """Download the ARC dataset from GitHub."""
    sys.stdout.write("=" * 70 + "\n")
    sys.stdout.write("ARC Prize Workflow - Step 1: Download Dataset\n")
    sys.stdout.write("=" * 70 + "\n\n")

    # Create data directory
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        sys.stdout.write(f"✓ Created directory: {DATA_DIR}/\n")
    else:
        sys.stdout.write(f"✓ Directory already exists: {DATA_DIR}/\n")

    # Download dataset
    zip_path = os.path.join(DATA_DIR, ZIP_FILE)

    if os.path.exists(zip_path):
        sys.stdout.write(f"✓ Dataset already downloaded: {zip_path}\n")
    else:
        sys.stdout.write(f"Downloading ARC dataset from GitHub...\n")
        sys.stdout.write(f"URL: {ARC_DATASET_URL}\n")

        try:
            urllib.request.urlretrieve(ARC_DATASET_URL, zip_path)
            sys.stdout.write(f"✓ Downloaded successfully: {zip_path}\n")
        except Exception as e:
            sys.stderr.write(f"✗ Download failed: {e}\n")
            sys.exit(1)

    # Extract dataset
    extract_dir = os.path.join(DATA_DIR, "ARC-master")

    if os.path.exists(extract_dir):
        sys.stdout.write(f"✓ Dataset already extracted: {extract_dir}/\n")
    else:
        sys.stdout.write(f"Extracting dataset...\n")

        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(DATA_DIR)
            sys.stdout.write(f"✓ Extracted successfully: {extract_dir}/\n")
        except Exception as e:
            sys.stderr.write(f"✗ Extraction failed: {e}\n")
            sys.exit(1)

    # Verify dataset structure
    sys.stdout.write("\n")
    sys.stdout.write("Verifying dataset structure...\n")

    training_dir = os.path.join(extract_dir, "data", "training")
    evaluation_dir = os.path.join(extract_dir, "data", "evaluation")
    test_dir = os.path.join(extract_dir, "data", "test")

    training_files = []
    evaluation_files = []
    test_files = []

    if os.path.exists(training_dir):
        training_files = [f for f in os.listdir(training_dir) if f.endswith('.json')]
        sys.stdout.write(f"✓ Training set: {len(training_files)} tasks\n")
    else:
        sys.stderr.write(f"✗ Training directory not found: {training_dir}\n")

    if os.path.exists(evaluation_dir):
        evaluation_files = [f for f in os.listdir(evaluation_dir) if f.endswith('.json')]
        sys.stdout.write(f"✓ Evaluation set: {len(evaluation_files)} tasks\n")
    else:
        sys.stderr.write(f"✗ Evaluation directory not found: {evaluation_dir}\n")

    if os.path.exists(test_dir):
        test_files = [f for f in os.listdir(test_dir) if f.endswith('.json')]
        sys.stdout.write(f"✓ Test set: {len(test_files)} tasks\n")
    else:
        # Test directory might not exist in some versions
        sys.stdout.write(f"⚠ Test directory not found (might not be included)\n")

    # Show example task
    sys.stdout.write("\n")
    sys.stdout.write("Example task structure:\n")

    if training_files:
        example_file = os.path.join(training_dir, training_files[0])
        with open(example_file, 'r') as f:
            example_task = json.load(f)

        sys.stdout.write(f"File: {training_files[0]}\n")
        sys.stdout.write(f"Training examples: {len(example_task.get('train', []))}\n")
        sys.stdout.write(f"Test examples: {len(example_task.get('test', []))}\n")

        if example_task.get('train'):
            train_example = example_task['train'][0]
            input_grid = train_example.get('input', [])
            output_grid = train_example.get('output', [])
            sys.stdout.write(f"Input grid size: {len(input_grid)}x{len(input_grid[0]) if input_grid else 0}\n")
            sys.stdout.write(f"Output grid size: {len(output_grid)}x{len(output_grid[0]) if output_grid else 0}\n")

    # Summary
    sys.stdout.write("\n")
    sys.stdout.write("=" * 70 + "\n")
    sys.stdout.write("✓ Dataset download complete!\n")
    sys.stdout.write("=" * 70 + "\n\n")

    sys.stdout.write("Next steps:\n")
    sys.stdout.write("  1. Review the dataset in: data/ARC-master/data/\n")
    sys.stdout.write("  2. Run training with Worm Python: worm 02_train_model.py\n")
    sys.stdout.write("  3. Evaluate your model: worm 03_evaluate.py\n")
    sys.stdout.write("\n")

    sys.stdout.write("Dataset paths:\n")
    sys.stdout.write(f"  Training: {training_dir}\n")
    sys.stdout.write(f"  Evaluation: {evaluation_dir}\n")
    if os.path.exists(test_dir):
        sys.stdout.write(f"  Test: {test_dir}\n")
    sys.stdout.write("\n")


if __name__ == '__main__':
    download_dataset()
