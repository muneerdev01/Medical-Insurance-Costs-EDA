#!/bin/bash
# Quick Start Script for Insurance Dashboard

echo "=========================================="
echo "Medical Insurance Dashboard - Quick Start"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "ERROR: Python is not installed or not in PATH"
    exit 1
fi

echo "✓ Python found"

# Install requirements
echo ""
echo "Installing required packages..."
pip install -r requirements.txt

# Check installation
if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

# Launch dashboard
echo ""
echo "=========================================="
echo "Launching Streamlit Dashboard..."
echo "=========================================="
echo ""
echo "The dashboard will open in your default browser at http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run dashboard.py
