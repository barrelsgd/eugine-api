#!/usr/bin/env bash

# Pre-deployment validation script
# Runs all checks before deploying to production

set -e  # Exit on error

echo "=========================================="
echo "🚀 Pre-Deployment Validation Starting..."
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track failures
FAILURES=0

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $2"
    else
        echo -e "${RED}✗${NC} $2"
        FAILURES=$((FAILURES + 1))
    fi
}

# 1. Check environment variables
echo "📋 Step 1: Checking environment variables..."
if [ ! -f .env ]; then
    print_status 1 ".env file missing"
else
    print_status 0 ".env file exists"
    
    # Check for default secrets
    if grep -q "SECRET_KEY=changethis" .env 2>/dev/null; then
        print_status 1 "SECRET_KEY is still set to default 'changethis'"
    else
        print_status 0 "SECRET_KEY is configured"
    fi
    
    if grep -q "POSTGRES_PASSWORD=changethis" .env 2>/dev/null; then
        print_status 1 "POSTGRES_PASSWORD is still set to default 'changethis'"
    else
        print_status 0 "POSTGRES_PASSWORD is configured"
    fi
    
    if grep -q "FIRST_SUPERUSER_PASSWORD=changethis" .env 2>/dev/null; then
        print_status 1 "FIRST_SUPERUSER_PASSWORD is still set to default 'changethis'"
    else
        print_status 0 "FIRST_SUPERUSER_PASSWORD is configured"
    fi
fi
echo ""

# 2. Code formatting check
echo "🎨 Step 2: Checking code formatting..."
if docker compose exec -T api uv run ruff format src --check > /dev/null 2>&1; then
    print_status 0 "Code formatting is correct"
else
    print_status 1 "Code formatting issues found (run: ./scripts/format.sh)"
fi
echo ""

# 3. Linting check
echo "🔍 Step 3: Running linter..."
if docker compose exec -T api uv run ruff check src > /dev/null 2>&1; then
    print_status 0 "No linting errors"
else
    print_status 1 "Linting errors found (run: docker compose exec api uv run ruff check src)"
fi
echo ""

# 4. Type checking
echo "🔎 Step 4: Running type checker..."
if docker compose exec -T api uv run mypy src > /dev/null 2>&1; then
    print_status 0 "Type checking passed"
else
    print_status 1 "Type checking failed (run: docker compose exec api uv run mypy src)"
fi
echo ""

# 5. Database migrations check
echo "🗄️  Step 5: Checking database migrations..."
MIGRATION_STATUS=$(docker compose exec -T api uv run alembic current 2>&1)
if echo "$MIGRATION_STATUS" | grep -q "head"; then
    print_status 0 "Database is up to date"
else
    print_status 1 "Database migrations pending (run: docker compose exec api uv run alembic upgrade head)"
fi
echo ""

# 6. Run tests
echo "🧪 Step 6: Running tests..."
if docker compose exec -T api uv run pytest tests/ -v > /dev/null 2>&1; then
    print_status 0 "All tests passed"
else
    print_status 1 "Tests failed (run: docker compose exec api uv run pytest tests/ -v)"
fi
echo ""

# 7. Check API health
echo "🏥 Step 7: Checking API health..."
if curl -s http://localhost:8000/api/v1/utils/health-check/ > /dev/null 2>&1; then
    print_status 0 "API is responding"
else
    print_status 1 "API is not responding (is it running?)"
fi
echo ""

# 8. Check for security issues
echo "🔒 Step 8: Security checks..."
# Check for hardcoded secrets in code
if grep -r "password.*=.*['\"].*['\"]" src/ --include="*.py" | grep -v "FIRST_SUPERUSER_PASSWORD" | grep -v "password:" > /dev/null 2>&1; then
    print_status 1 "Potential hardcoded passwords found in code"
else
    print_status 0 "No hardcoded passwords detected"
fi

# Check for debug mode
if grep -r "debug.*=.*True" src/ --include="*.py" > /dev/null 2>&1; then
    print_status 1 "Debug mode enabled in code"
else
    print_status 0 "Debug mode not found in code"
fi
echo ""

# 9. Check Docker build
echo "🐳 Step 9: Checking Docker build..."
if docker compose build api > /dev/null 2>&1; then
    print_status 0 "Docker build successful"
else
    print_status 1 "Docker build failed"
fi
echo ""

# 10. Check dependencies
echo "📦 Step 10: Checking dependencies..."
if docker compose exec -T api uv pip check > /dev/null 2>&1; then
    print_status 0 "No dependency conflicts"
else
    print_status 1 "Dependency conflicts detected"
fi
echo ""

# Summary
echo "=========================================="
if [ $FAILURES -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed! Ready for deployment.${NC}"
    echo "=========================================="
    exit 0
else
    echo -e "${RED}✗ $FAILURES check(s) failed. Please fix before deploying.${NC}"
    echo "=========================================="
    exit 1
fi
