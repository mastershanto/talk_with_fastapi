#!/bin/bash

# Quick Start Script for FastAPI ML Project
# This script will set up and run the application

set -e  # Exit on error

echo "=========================================="
echo "FastAPI ML CRUD Application Setup"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 is installed"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Train ML model if it doesn't exist
if [ ! -f "model/iris_model.joblib" ]; then
    echo "🤖 Training ML model..."
    python -m model.train_model
    echo "✓ Model trained and saved"
else
    echo "✓ ML model already exists"
fi

# Check if database exists
if [ ! -f "test.db" ]; then
    echo "🗄️  Database will be created on first run"
fi

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "To start the application, run:"
echo "  source venv/bin/activate"
echo "  python -m uvicorn src.main:app --reload"
echo ""
echo "Then visit:"
echo "  • API Docs: http://localhost:8000/docs"
echo "  • Application: http://localhost:8000"
echo ""
echo "To run tests:"
echo "  pytest tests/ -v"
echo ""
