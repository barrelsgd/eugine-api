# Testing & Pre-Deployment Guide

This guide covers all testing and validation steps before deploying your FastAPI application.

## Quick Start

### Run All Pre-Deployment Checks

**Linux/Mac:**
```bash
chmod +x scripts/pre-deploy.sh
./scripts/pre-deploy.sh
```

**Windows (PowerShell):**
```powershell
.\scripts\pre-deploy.ps1
```

**Windows (Git Bash):**
```bash
bash scripts/pre-deploy.sh
```

## Individual Test Commands

### 1. Code Formatting

**Check formatting:**
```bash
docker compose exec api uv run ruff format src --check
```

**Auto-fix formatting:**
```bash
docker compose exec api uv run ruff format src
# Or use the script:
./scripts/format.sh
```

### 2. Linting

**Check for code issues:**
```bash
docker compose exec api uv run ruff check src
```

**Auto-fix linting issues:**
```bash
docker compose exec api uv run ruff check src --fix
```

### 3. Type Checking

**Run mypy:**
```bash
docker compose exec api uv run mypy src
```

### 4. Run Tests

**Run all tests:**
```bash
docker compose exec api uv run pytest
```

**Run with verbose output:**
```bash
docker compose exec api uv run pytest -v
```

**Run specific test file:**
```bash
docker compose exec api uv run pytest tests/api/test_items.py
```

**Run with coverage:**
```bash
docker compose exec api uv run pytest --cov=src --cov-report=html
```

**View coverage report:**
Open `htmlcov/index.html` in your browser after running coverage.

### 5. Database Migrations

**Check current migration:**
```bash
docker compose exec api uv run alembic current
```

**Create new migration:**
```bash
docker compose exec api uv run alembic revision --autogenerate -m "description"
```

**Apply migrations:**
```bash
docker compose exec api uv run alembic upgrade head
```

**Rollback migration:**
```bash
docker compose exec api uv run alembic downgrade -1
```

### 6. API Health Check

**Test API is running:**
```bash
curl http://localhost:8000/api/v1/utils/health-check/
```

**Test authentication:**
```bash
curl -X POST http://localhost:8000/api/v1/login/access-token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=changethis"
```

### 7. Security Checks

**Check for hardcoded secrets:**
```bash
# Linux/Mac
grep -r "password.*=.*['\"]" src/ --include="*.py"

# Windows (PowerShell)
Select-String -Path "src\**\*.py" -Pattern 'password.*=.*[''"]'
```

**Check environment variables:**
```bash
# Make sure these are NOT set to "changethis" in production
grep "changethis" .env
```

### 8. Dependency Check

**Check for conflicts:**
```bash
docker compose exec api uv pip check
```

**Update dependencies:**
```bash
docker compose exec api uv pip install --upgrade -r requirements.txt
```

## Pre-Deployment Checklist

Before deploying to production, ensure:

### ✅ Code Quality
- [ ] All tests pass
- [ ] Code is formatted (ruff format)
- [ ] No linting errors (ruff check)
- [ ] Type checking passes (mypy)
- [ ] Code coverage > 80%

### ✅ Security
- [ ] `SECRET_KEY` is changed from "changethis"
- [ ] `POSTGRES_PASSWORD` is changed from "changethis"
- [ ] `FIRST_SUPERUSER_PASSWORD` is changed from "changethis"
- [ ] No hardcoded secrets in code
- [ ] Debug mode is disabled
- [ ] CORS origins are properly configured
- [ ] HTTPS is enabled in production

### ✅ Database
- [ ] All migrations are applied
- [ ] Database backup is created
- [ ] Migration rollback plan exists

### ✅ Environment
- [ ] `.env` file is configured for production
- [ ] Environment variables are set correctly
- [ ] Sentry DSN is configured (if using)
- [ ] Email settings are configured (if using)

### ✅ Docker
- [ ] Docker build succeeds
- [ ] All containers start successfully
- [ ] Health check endpoint responds
- [ ] Logs show no errors

### ✅ API
- [ ] OpenAPI docs are accessible
- [ ] All endpoints return expected responses
- [ ] Authentication works correctly
- [ ] Rate limiting is configured (if needed)

## Testing Best Practices

### Writing Tests

Follow these patterns when writing tests:

```python
# tests/api/test_items.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

def test_create_item(client: TestClient, superuser_token_headers: dict):
    """Test creating an item."""
    data = {"title": "Test Item", "content": "Test content"}
    response = client.post(
        "/api/v1/items/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert "id" in content
```

### Test Organization

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── api/                     # API endpoint tests
│   ├── __init__.py
│   ├── test_items.py
│   ├── test_users.py
│   └── test_login.py
├── crud/                    # Service layer tests
│   ├── __init__.py
│   ├── test_item_service.py
│   └── test_user_service.py
└── utils/                   # Utility function tests
    ├── __init__.py
    └── test_security.py
```

### Fixtures

Common fixtures in `conftest.py`:

```python
@pytest.fixture
def client() -> Generator:
    with TestClient(app) as c:
        yield c

@pytest.fixture
def db() -> Generator:
    with Session(engine) as session:
        yield session

@pytest.fixture
def superuser_token_headers(client: TestClient) -> dict:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post("/api/v1/login/access-token", data=login_data)
    tokens = r.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run pre-deployment checks
        run: |
          docker compose up -d
          ./scripts/pre-deploy.sh
```

## Troubleshooting

### Tests Failing

1. **Check database is running:**
   ```bash
   docker compose ps
   ```

2. **Reset database:**
   ```bash
   docker compose down -v
   docker compose up -d
   ```

3. **Check logs:**
   ```bash
   docker compose logs api
   ```

### Linting Errors

**Auto-fix most issues:**
```bash
docker compose exec api uv run ruff check src --fix
docker compose exec api uv run ruff format src
```

### Type Errors

**Common fixes:**
- Add type hints to function parameters
- Use `Optional[Type]` for nullable values
- Import types from `typing` module

### Migration Errors

**Reset migrations (development only):**
```bash
# WARNING: This deletes all data
docker compose down -v
docker compose up -d
docker compose exec api uv run alembic upgrade head
```

## Performance Testing

### Load Testing with Locust

```python
# locustfile.py
from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def health_check(self):
        self.client.get("/api/v1/utils/health-check/")
    
    @task(3)
    def list_items(self):
        self.client.get("/api/v1/items/")
```

**Run load test:**
```bash
locust -f locustfile.py --host=http://localhost:8000
```

## Monitoring

### Check Application Metrics

```bash
# API response time
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/api/v1/utils/health-check/

# Database connections
docker compose exec db psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"

# Container stats
docker stats
```

## Additional Resources

- [FastAPI Testing Documentation](https://fastapi.tiangolo.com/tutorial/testing/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [MyPy Documentation](https://mypy.readthedocs.io/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

## Summary

**Quick commands for daily development:**

```bash
# Format code
./scripts/format.sh

# Run tests
docker compose exec api uv run pytest -v

# Check everything before commit
./scripts/pre-deploy.sh

# Create migration
docker compose exec api uv run alembic revision --autogenerate -m "description"

# Apply migrations
docker compose exec api uv run alembic upgrade head
```

**Before every deployment:**
```bash
./scripts/pre-deploy.sh
```

If all checks pass ✅, you're ready to deploy! 🚀
