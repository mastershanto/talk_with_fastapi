#!/bin/bash

# One-time local setup script for this repository.

set -e

echo "=========================================="
echo "Talk With FastAPI - Local Setup"
echo "=========================================="
echo ""

if ! command -v python3 >/dev/null 2>&1; then
    echo "❌ Python 3 is not installed."
    exit 1
fi

if [ ! -d ".venv" ]; then
    echo "📦 Creating .venv ..."
    python3 -m venv .venv
else
    echo "✓ .venv already exists"
fi

echo "🔄 Activating virtual environment..."
source .venv/bin/activate

echo "📥 Installing dependencies..."
python -m pip install -U pip
python -m pip install -r requirements-dev.txt

echo "🪝 Installing pre-commit hooks..."
pre-commit install

echo "✅ Running local quality checks..."
make ci

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Start server:"
echo "  bash scripts/run.sh"
echo ""
echo "Docs:"
echo "  http://localhost:8000/docs"
