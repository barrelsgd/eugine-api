# 📜 Scripts Documentation

This folder contains all development, deployment, and maintenance scripts for the FastAPI project.

---

## 🚀 Quick Start

### First Time Setup
```bash
./scripts/setup.sh
```

### Daily Development
```bash
# Start development environment
./scripts/dev.sh start

# Or use watch mode
docker compose watch
```

### Common Tasks
```bash
# Format code
./scripts/format.sh

# Check code quality
./scripts/lint.sh

# Run tests
./scripts/test.sh

# Quick API test
docker compose exec api python scripts/quick_test.py
```

---

## 📚 Scripts Reference

### 🔧 Development Scripts

#### `dev.sh` - Development Helper (⭐ Main Tool)
**Your primary development command center.**

```bash
./scripts/dev.sh [command]
```

**Commands:**
- `start` - Start all services with watch mode
- `stop` - Stop all services
- `restart` - Restart all services
- `logs` - Show logs from all services
- `logs-api` - Show API logs only
- `logs-db` - Show database logs only
- `shell` - Open shell in API container
- `db-shell` - Open PostgreSQL shell
- `migrate` - Run database migrations
- `migration "message"` - Create new migration
- `test` - Run tests
- `test-cov` - Run tests with coverage
- `clean` - Stop and remove all containers and volumes
- `rebuild` - Rebuild containers from scratch
- `status` - Show status of all services

**Examples:**
```bash
./scripts/dev.sh start          # Start development
./scripts/dev.sh logs-api       # Watch API logs
./scripts/dev.sh shell          # Open shell in container
./scripts/dev.sh migration "add user roles"  # Create migration
./scripts/dev.sh test-cov       # Run tests with coverage
```

#### `setup.sh` - Initial Setup
**Run this once when setting up the project.**

```bash
./scripts/setup.sh
```

**What it does:**
- Checks if Docker is running
- Verifies Docker Compose is available
- Creates `.env` file from example
- Creates necessary Docker networks
- Provides next steps instructions

---

### 🎨 Code Quality Scripts

#### `format.sh` - Code Formatting
**Auto-format your code with Ruff.**

```bash
./scripts/format.sh
```

**What it does:**
- Fixes auto-fixable linting issues
- Formats all code in `src/` and `scripts/`
- Uses Ruff for fast, modern formatting

#### `lint.sh` - Code Quality Checks
**Comprehensive code quality validation.**

```bash
./scripts/lint.sh
```

**Checks:**
- ✅ Type checking with `mypy`
- ✅ Linting with `ruff check`
- ✅ Format checking with `ruff format --check`

**Exit codes:**
- `0` - All checks passed
- `1` - One or more checks failed

#### `pre-deploy.sh` - Pre-Deployment Validation
**Run before deploying to production.**

```bash
./scripts/pre-deploy.sh
```

**10-Step Validation:**
1. Environment variables check
2. Code formatting check
3. Linting check
4. Type checking
5. Database migrations check
6. Tests execution
7. API health check
8. Security checks (hardcoded secrets, debug mode)
9. Docker build check
10. Dependencies check

---

### 🧪 Testing Scripts

#### `test.sh` - Test Suite
**Run full test suite with coverage.**

```bash
./scripts/test.sh
```

**What it does:**
- Checks if API is running (optional)
- Runs pytest with coverage
- Generates coverage report
- Creates HTML coverage report in `htmlcov/`

#### `quick_test.py` - API Smoke Tests
**Fast API validation tests.**

```bash
docker compose exec api python scripts/quick_test.py
```

**7 Tests:**
1. ✅ API Health Check
2. ✅ Router Structure (6 tag groups)
3. ✅ Enhanced Documentation
4. ✅ User Registration
5. ✅ Login Flow
6. ✅ Authenticated Endpoints
7. ✅ Constants Usage

**Perfect for:**
- Quick validation after changes
- CI/CD pipelines
- Deployment verification

---

### 🗄️ Database Scripts

#### `db.sh` - Database Management
**All your database operations in one place.**

```bash
./scripts/db.sh [command]
```

**Commands:**
- `shell` - Open PostgreSQL shell
- `backup` - Create timestamped database backup
- `restore <file>` - Restore database from backup
- `reset` - Reset database (⚠️ deletes all data)
- `migrate` - Run migrations
- `migration "message"` - Create new migration
- `current` - Show current migration
- `history` - Show migration history
- `seed` - Seed database with test data

**Examples:**
```bash
./scripts/db.sh shell                    # Open psql
./scripts/db.sh backup                   # Create backup
./scripts/db.sh migration "add roles"    # Create migration
./scripts/db.sh migrate                  # Apply migrations
./scripts/db.sh seed                     # Add test data
./scripts/db.sh restore backups/db_backup_20241014_120000.sql
```

**Backup Location:**
Backups are saved in `backups/db_backup_YYYYMMDD_HHMMSS.sql`

#### `backend_pre_start.py` - Database Health Check
**Ensures database is ready before starting API.**

```bash
python scripts/backend_pre_start.py
```

**What it does:**
- Waits for database to be ready (up to 5 minutes)
- Uses retry logic with exponential backoff
- Called automatically by `prestart.sh`

#### `initial_data.py` - Initialize Database
**Creates initial superuser.**

```bash
python scripts/initial_data.py
```

**What it does:**
- Creates first superuser from env vars
- Safe to run multiple times (idempotent)
- Called automatically by `prestart.sh`

#### `seed_data.py` - Test Data Seeder
**Populate database with test data for development.**

```bash
python scripts/seed_data.py
# Or use db.sh
./scripts/db.sh seed
```

**What it creates:**
- 5 test users (testuser0@example.com to testuser4@example.com)
- 3 test items per user
- Password for all: `testpass123`

**Perfect for:**
- Development testing
- Demo environments
- Frontend development

---

### 🐳 Container Scripts

#### `prestart.sh` - Prestart Hook
**Runs automatically before API starts in container.**

```bash
./scripts/prestart.sh
```

**Execution Order:**
1. Check database connection
2. Run database migrations
3. Initialize database with superuser

**Used by:**
- Docker Compose (automatically)
- CI/CD pipelines
- Manual container initialization

---

### 🧹 Maintenance Scripts

#### `clean.sh` - Cleanup Development Artifacts
**Remove all cache and temporary files.**

```bash
./scripts/clean.sh
```

**What it removes:**
- Python cache (`__pycache__`, `*.pyc`, `*.pyo`)
- Coverage reports (`htmlcov/`, `.coverage`)
- Mypy cache (`.mypy_cache/`)
- Ruff cache (`.ruff_cache/`)
- Pytest cache (`.pytest_cache/`)
- Egg info (`*.egg-info/`)

**Safe to run anytime!**

---

### 🚢 Legacy Deployment Scripts

These scripts are for Docker Swarm deployments and may need updates for modern Docker Compose.

#### `build.sh` - Build Docker Images
```bash
TAG=v1.0.0 ./scripts/build.sh
```

#### `build-push.sh` - Build and Push Images
```bash
TAG=v1.0.0 ./scripts/build-push.sh
```

#### `deploy.sh` - Deploy to Docker Swarm
```bash
DOMAIN=api.example.com STACK_NAME=myapp TAG=v1.0.0 ./scripts/deploy.sh
```

**Note:** Consider updating these for modern Docker Compose or Kubernetes deployments.

---

## 🎯 Common Workflows

### Starting a New Feature
```bash
# 1. Update code
git checkout -b feature/new-feature

# 2. Format code
./scripts/format.sh

# 3. Check quality
./scripts/lint.sh

# 4. Run tests
./scripts/test.sh

# 5. Quick API test
docker compose exec api python scripts/quick_test.py
```

### Creating Database Changes
```bash
# 1. Modify models in src/*/models.py

# 2. Create migration
./scripts/db.sh migration "describe your changes"

# 3. Review generated migration in alembic/versions/

# 4. Apply migration
./scripts/db.sh migrate

# 5. Verify
./scripts/db.sh current
```

### Preparing for Deployment
```bash
# 1. Run pre-deployment checks
./scripts/pre-deploy.sh

# 2. If all pass, create backup
./scripts/db.sh backup

# 3. Deploy!
```

### Debugging Issues
```bash
# View logs
./scripts/dev.sh logs-api

# Open shell in container
./scripts/dev.sh shell

# Check database
./scripts/db.sh shell

# Run quick tests
docker compose exec api python scripts/quick_test.py
```

### Resetting Everything
```bash
# Clean code artifacts
./scripts/clean.sh

# Reset Docker environment
./scripts/dev.sh clean

# Rebuild from scratch
./scripts/dev.sh rebuild

# Start fresh
./scripts/dev.sh start
```

---

## 🔑 Environment Variables

Scripts that require environment variables will load them from `.env` file.

**Key variables:**
- `POSTGRES_USER` - Database user
- `POSTGRES_PASSWORD` - Database password
- `POSTGRES_DB` - Database name
- `SECRET_KEY` - Application secret key
- `FIRST_SUPERUSER` - Initial superuser email
- `FIRST_SUPERUSER_PASSWORD` - Initial superuser password

---

## 🎓 Best Practices

### When to Use Each Script

**Daily Development:**
- `dev.sh start` - Start your day
- `format.sh` - Before committing
- `lint.sh` - Before pushing
- `quick_test.py` - After making changes

**Working with Database:**
- `db.sh backup` - Before major changes
- `db.sh migration` - When changing models
- `db.sh seed` - When testing features
- `db.sh shell` - When investigating data

**Code Quality:**
- `format.sh` - Automatically fix formatting
- `lint.sh` - Check for issues
- `test.sh` - Full test suite with coverage
- `pre-deploy.sh` - Before deploying

**Maintenance:**
- `clean.sh` - When disk space is low
- `dev.sh clean` - When containers misbehave
- `dev.sh rebuild` - When Dockerfile changes

---

## 💡 Tips & Tricks

### Create Aliases
Add to your `.bashrc` or `.zshrc`:
```bash
alias fd='./scripts/dev.sh'
alias ftest='docker compose exec api python scripts/quick_test.py'
alias flint='./scripts/lint.sh'
alias fformat='./scripts/format.sh'
alias fdb='./scripts/db.sh'
```

### Make Scripts Executable
```bash
chmod +x scripts/*.sh
```

### Auto-format on Save
Configure your IDE to run `./scripts/format.sh` on save.

### Watch Logs in Real-time
```bash
./scripts/dev.sh logs-api | grep ERROR
```

### Quick Database Reset for Testing
```bash
./scripts/db.sh reset && ./scripts/db.sh seed
```

---

## 📊 Script Status

| Script | Status | Quality | Purpose |
|--------|--------|---------|---------|
| `dev.sh` | ⭐⭐⭐⭐⭐ | Excellent | Main dev tool |
| `setup.sh` | ⭐⭐⭐⭐⭐ | Excellent | Initial setup |
| `pre-deploy.sh` | ⭐⭐⭐⭐⭐ | Excellent | Pre-deploy validation |
| `format.sh` | ⭐⭐⭐⭐⭐ | Updated | Code formatting |
| `lint.sh` | ⭐⭐⭐⭐⭐ | Updated | Code quality |
| `test.sh` | ⭐⭐⭐⭐⭐ | Updated | Testing |
| `prestart.sh` | ⭐⭐⭐⭐⭐ | Updated | Container init |
| `db.sh` | ⭐⭐⭐⭐⭐ | New | Database mgmt |
| `seed_data.py` | ⭐⭐⭐⭐⭐ | New | Test data |
| `clean.sh` | ⭐⭐⭐⭐⭐ | New | Cleanup |
| `quick_test.py` | ⭐⭐⭐⭐⭐ | Excellent | API testing |
| `backend_pre_start.py` | ⭐⭐⭐⭐ | Good | DB health |
| `initial_data.py` | ⭐⭐⭐⭐ | Good | DB init |

---

## 🆘 Troubleshooting

### "Permission denied"
```bash
chmod +x scripts/*.sh
```

### "Docker is not running"
Start Docker Desktop or Docker daemon.

### "Database connection failed"
```bash
docker compose up -d db
# Wait a few seconds
./scripts/dev.sh status
```

### "Module not found" errors
```bash
docker compose exec api uv sync
```

### Tests failing
```bash
# Check API is running
./scripts/dev.sh status

# View logs
./scripts/dev.sh logs-api

# Reset if needed
./scripts/db.sh reset
```

---

## 📞 Need Help?

1. Check script help: `./scripts/<script>.sh --help`
2. View this README
3. Check `SCRIPTS_ANALYSIS.md` for detailed analysis
4. Review `IMPLEMENTATION_COMPLETE.md` for project overview

---

**Last Updated:** October 14, 2025  
**Maintained by:** Project Team  
**Status:** ✅ Production Ready

