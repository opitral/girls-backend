#!/bin/bash

set -e

echo "🐍 Activating virtual environment..."
source venv/bin/activate

echo "🚀 Running main.py..."
python3 main.py
