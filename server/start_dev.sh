#!/bin/bash

# Activate Python virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate || { echo "❌ Failed to activate venv. Did you run 'python -m venv venv'?" ; exit 1; }

# Load environment variables from .env
if [ -f .env ]; then
    echo "🌱 Loading environment variables from .env"
    export $(grep -v '^#' .env | xargs)
else
    echo "⚠️ .env file not found. Skipping environment variables load."
fi

# Start Flask dev server
echo "🚀 Starting Flask development server..."
python app.py

