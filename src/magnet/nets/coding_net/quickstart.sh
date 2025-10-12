#!/bin/bash
# Quick start script for coding_net

echo "🚀 Coding Net Ensemble - Quick Start"
echo "===================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Check for OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo ""
    echo "⚠️  Warning: OPENAI_API_KEY not set!"
    echo "Please set it with: export OPENAI_API_KEY='your-key-here'"
    echo ""
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Available commands:"
echo "  Test:        python test.py"
echo "  Interactive: python -m magnet.nets.coding_net.app"
echo "  Quick test:  python -m magnet.nets.coding_net.app --profile quick_test"
echo "  Help:        python -m magnet.nets.coding_net.app --help"
echo ""
