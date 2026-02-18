#!/bin/bash
# Simple script to run FastAPI server

echo "🚀 Starting FastAPI server..."

# Activate virtual environment
source .venv/bin/activate

# Run uvicorn server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
