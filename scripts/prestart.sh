#!/bin/bash

echo "Running prestart script..."

# Let the DB start
echo "Checking database connection..."
uv run python scripts/backend_pre_start.py

# Run database migrations
echo "Running database migrations..."
uv run alembic upgrade head

# Initialize database with first superuser
echo "Initializing database..."
uv run python scripts/initial_data.py

echo "Prestart script completed successfully!"
