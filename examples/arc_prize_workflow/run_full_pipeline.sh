#!/bin/bash
# ARC Prize Workflow - Full Pipeline Runner
#
# This script runs the complete workflow from download to submission.
# Use this for iterative development and testing.

set -e

echo "╔═══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                       ║"
echo "║              ARC PRIZE WORKFLOW - FULL PIPELINE                       ║"
echo "║              Worm Python Hybrid Security Model                        ║"
echo "║                                                                       ║"
echo "╚═══════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Worm Python is installed
if ! command -v worm &> /dev/null; then
    echo "✗ Worm Python not found in PATH"
    echo "  Install with: cd ../.. && ./scripts/install.sh"
    exit 1
fi

echo "✓ Worm Python installed"
echo ""

# Step 1: Download dataset (if needed)
echo "────────────────────────────────────────────────────────────────────────"
echo "Step 1: Download Dataset (Standard Python)"
echo "────────────────────────────────────────────────────────────────────────"
echo ""

if [ -d "data/ARC-master" ]; then
    echo "✓ Dataset already downloaded"
    echo "  Skip step 1 (use --force to re-download)"
else
    echo "Downloading dataset..."
    python3 01_download_dataset.py
fi

echo ""

# Step 2: Train model
echo "────────────────────────────────────────────────────────────────────────"
echo "Step 2: Train Model (Worm Python - Secure)"
echo "────────────────────────────────────────────────────────────────────────"
echo ""

worm 02_train_model.py

echo ""

# Step 3: Evaluate
echo "────────────────────────────────────────────────────────────────────────"
echo "Step 3: Evaluate Model (Worm Python - Secure)"
echo "────────────────────────────────────────────────────────────────────────"
echo ""

worm 03_evaluate.py

echo ""

# Step 4: Generate predictions
echo "────────────────────────────────────────────────────────────────────────"
echo "Step 4: Generate Predictions (Worm Python - Secure)"
echo "────────────────────────────────────────────────────────────────────────"
echo ""

worm 04_generate_predictions.py

echo ""

# Step 5: Submit (interactive)
echo "────────────────────────────────────────────────────────────────────────"
echo "Step 5: Submit to Competition (Standard Python)"
echo "────────────────────────────────────────────────────────────────────────"
echo ""

echo "Ready to submit!"
echo ""
echo "Run: python3 05_submit.py"
echo "Or upload results/predictions.json to the competition website"
echo ""

# Summary
echo "╔═══════════════════════════════════════════════════════════════════════╗"
echo "║                       PIPELINE COMPLETE!                              ║"
echo "╚═══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Generated files:"
echo "  • models/model_info.json           - Model metadata"
echo "  • results/evaluation_results.json  - Evaluation results"
echo "  • results/predictions.json         - Ready for submission"
echo "  • results/submission_metadata.json - Submission metadata"
echo ""
echo "Next steps:"
echo "  1. Review results: cat results/evaluation_results.json"
echo "  2. Submit: python3 05_submit.py"
echo ""
echo "Security summary:"
echo "  ✓ Steps 2-4 ran in Worm Python (secure, no network)"
echo "  ✓ Training data protected from exfiltration"
echo "  ✓ Predictions generated locally"
echo "  ✓ Ready for manual submission"
echo ""
