#!/bin/bash
# Install stock-data-skill CLI
# Requires: Python 3.10+, uv or pip

set -e

if command -v uv &> /dev/null; then
    echo "Installing with uv..."
    uv pip install stock-data-skill
elif command -v pip &> /dev/null; then
    echo "Installing with pip..."
    pip install stock-data-skill
else
    echo "Error: Neither uv nor pip found. Please install Python 3.10+ first."
    exit 1
fi

echo ""
echo "Installation complete!"
echo ""
echo "Quick start:"
echo "  stock-data --list              # List all tools"
echo "  stock-data get_current_time    # Test basic call"
echo ""
echo "Configure API keys (optional):"
echo "  cp .env.example ~/.stock-data.env"
echo "  # Edit ~/.stock-data.env with your API keys"
