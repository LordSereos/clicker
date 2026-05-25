#!/bin/bash
set -e

echo "Checking prerequisites..."

# Python 3
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 is not installed. Install it from https://www.python.org or via Homebrew: brew install python3"
    exit 1
fi
echo "  python3: $(python3 --version)"

# pip3
if ! command -v pip3 &>/dev/null; then
    echo "ERROR: pip3 is not installed. It usually comes with Python 3."
    exit 1
fi
echo "  pip3: $(pip3 --version | awk '{print $1, $2}')"

# Install dependencies from requirements.txt
echo "Installing dependencies..."
pip3 install -r "$(dirname "$0")/requirements.txt"

echo ""
echo "All dependencies installed."
echo ""
echo "IMPORTANT: Grant Accessibility permissions to your terminal app before running macro.py:"
echo "  System Settings -> Privacy & Security -> Accessibility -> add Terminal (or iTerm2, etc.)"
