#!/bin/bash

# Image Import Script
# This script handles venv setup, dependencies, and image importing

set -e  # Exit on error

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_DIR="$PROJECT_ROOT/venv"
REQUIREMENTS_FILE="$PROJECT_ROOT/requirements.txt"

echo "==================================="
echo "Photography Portfolio Image Importer"
echo "==================================="
echo ""

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Creating venv..."
    python3 -m venv "$VENV_DIR"
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment found"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Install/update dependencies
echo "Installing dependencies from requirements.txt..."
pip install --quiet --upgrade pip
pip install --quiet -r "$REQUIREMENTS_FILE"
echo "✓ Dependencies installed"

echo ""
echo "Starting image import process..."
echo "==================================="
echo ""

# Run the converter script
python3 "$SCRIPT_DIR/converterscript.py"

echo ""
echo "==================================="
echo "Image import complete!"
echo "==================================="

# Deactivate virtual environment
deactivate
