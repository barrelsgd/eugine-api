#!/usr/bin/env bash
# Clean up development artifacts

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "🧹 Cleaning development artifacts..."
echo ""

# Remove Python cache
echo "Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
echo "✅ Python cache removed"

# Remove coverage files
if [ -d "htmlcov" ]; then
    echo "Removing coverage reports..."
    rm -rf htmlcov .coverage
    echo "✅ Coverage reports removed"
fi

# Remove mypy cache
if [ -d ".mypy_cache" ]; then
    echo "Removing mypy cache..."
    rm -rf .mypy_cache
    echo "✅ Mypy cache removed"
fi

# Remove ruff cache
if [ -d ".ruff_cache" ]; then
    echo "Removing ruff cache..."
    rm -rf .ruff_cache
    echo "✅ Ruff cache removed"
fi

# Remove pytest cache
if [ -d ".pytest_cache" ]; then
    echo "Removing pytest cache..."
    rm -rf .pytest_cache
    echo "✅ Pytest cache removed"
fi

# Remove egg-info
if [ -d "src/*.egg-info" ]; then
    echo "Removing egg-info..."
    rm -rf src/*.egg-info
    echo "✅ Egg-info removed"
fi

echo ""
echo "✅ Cleanup complete!"

