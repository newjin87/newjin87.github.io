#!/bin/bash
# Script to run the Daily Briefing Automation with the correct Python environment

# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navigate to the automation directory
cd "$DIR"

# Check if .venv exists
if [ ! -d ".venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv .venv
    source .venv/bin/activate
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi

# Run the main script
echo "🚀 Starting Daily Briefing Automation..."
python run_daily_briefing.py
