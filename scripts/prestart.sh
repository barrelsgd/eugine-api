#!/bin/bash
# Prestart script - runs before the API starts

set -e

echo "🚀 Running prestart script..."
echo ""

# Ensure we're in the right directory
cd /app

# Sync dependencies (install package + all dependencies)
echo "📦 Syncing dependencies..."
uv sync --frozen

# Let the DB start
echo "🗄️  Checking database connection..."
if uv run python scripts/backend_pre_start.py; then
    echo "✅ Database is ready"
else
    echo "❌ Database connection failed"
    exit 1
fi
echo ""

# Run database migrations
echo "🔄 Running database migrations..."
if uv run alembic upgrade head; then
    echo "✅ Migrations applied"
else
    echo "❌ Migration failed"
    exit 1
fi
echo ""

# Initialize database with first superuser
echo "👤 Initializing database..."
if uv run python scripts/initial_data.py; then
    echo "✅ Initial data created"
else
    echo "⚠️  Initial data creation failed (may already exist)"
fi
echo ""

echo "✅ Prestart script completed successfully!"
exit 0
