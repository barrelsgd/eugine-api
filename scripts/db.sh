#!/usr/bin/env bash
# Database management helper

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

function print_help() {
    echo "Database Management Helper"
    echo ""
    echo "Usage: ./scripts/db.sh [command]"
    echo ""
    echo "Commands:"
    echo "  shell         Open PostgreSQL shell"
    echo "  backup        Create database backup"
    echo "  restore       Restore database from backup"
    echo "  reset         Reset database (WARNING: deletes all data)"
    echo "  migrate       Run migrations"
    echo "  migration     Create new migration"
    echo "  current       Show current migration"
    echo "  history       Show migration history"
    echo "  seed          Seed database with test data"
    echo ""
}

function db_shell() {
    echo -e "${GREEN}Opening PostgreSQL shell...${NC}"
    docker compose exec db psql -U app -d app
}

function backup() {
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="backups/db_backup_${TIMESTAMP}.sql"
    mkdir -p backups
    echo -e "${GREEN}Creating backup: ${BACKUP_FILE}${NC}"
    docker compose exec -T db pg_dump -U app app > "$BACKUP_FILE"
    echo -e "${GREEN}✓ Backup created successfully${NC}"
}

function restore() {
    if [ -z "$2" ]; then
        echo -e "${RED}Error: Backup file required${NC}"
        echo "Usage: ./scripts/db.sh restore <backup_file>"
        exit 1
    fi
    if [ ! -f "$2" ]; then
        echo -e "${RED}Error: Backup file not found: $2${NC}"
        exit 1
    fi
    echo -e "${YELLOW}Restoring from: $2${NC}"
    cat "$2" | docker compose exec -T db psql -U app app
    echo -e "${GREEN}✓ Database restored${NC}"
}

function reset_db() {
    echo -e "${RED}WARNING: This will delete all data!${NC}"
    read -p "Are you sure? Type 'yes' to confirm: " -r
    if [ "$REPLY" != "yes" ]; then
        echo "Cancelled"
        exit 0
    fi
    echo -e "${YELLOW}Resetting database...${NC}"
    docker compose down -v
    docker compose up -d db
    sleep 5
    docker compose up -d
    echo -e "${GREEN}✓ Database reset complete${NC}"
}

function migrate() {
    echo -e "${GREEN}Running migrations...${NC}"
    docker compose exec api uv run alembic upgrade head
    echo -e "${GREEN}✓ Migrations applied${NC}"
}

function migration() {
    if [ -z "$2" ]; then
        echo -e "${RED}Error: Migration message required${NC}"
        echo "Usage: ./scripts/db.sh migration \"message\""
        exit 1
    fi
    echo -e "${GREEN}Creating new migration: $2${NC}"
    docker compose exec api uv run alembic revision --autogenerate -m "$2"
    echo -e "${GREEN}✓ Migration created${NC}"
}

function current() {
    echo -e "${GREEN}Current migration:${NC}"
    docker compose exec api uv run alembic current
}

function history() {
    echo -e "${GREEN}Migration history:${NC}"
    docker compose exec api uv run alembic history --verbose
}

function seed() {
    echo -e "${GREEN}Seeding database with test data...${NC}"
    docker compose exec api python scripts/seed_data.py
    echo -e "${GREEN}✓ Database seeded${NC}"
}

case "$1" in
    shell) db_shell ;;
    backup) backup "$@" ;;
    restore) restore "$@" ;;
    reset) reset_db ;;
    migrate) migrate ;;
    migration) migration "$@" ;;
    current) current ;;
    history) history ;;
    seed) seed ;;
    help|--help|-h|"")
        print_help
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        echo ""
        print_help
        exit 1
        ;;
esac

