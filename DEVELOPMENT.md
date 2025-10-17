# FastAPI Project - Development Guide

This project follows [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices) structure with [FastAPI Full-Stack Template](https://github.com/fastapi/full-stack-fastapi-template) development workflow.

## Quick Start with Docker Compose Watch

Start the local stack with hot-reload enabled:

```bash
docker compose watch
```

This command will:
- Build and start all services (database, API, adminer, mailcatcher, traefik)
- Enable automatic file synchronization for instant updates
- Restart the API server when you change Python files
- Rebuild the container when `pyproject.toml` changes

## Available Services

Once running, access these URLs:

- **Backend API**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **API Documentation (ReDoc)**: http://localhost:8000/redoc
- **Adminer (Database UI)**: http://localhost:8080
- **MailCatcher (Email Testing)**: http://localhost:1080
- **Traefik Dashboard**: http://localhost:8090

## Docker Compose Watch Configuration

The watch mode is configured with:

### Sync Actions (Instant Updates)
- `./src` → `/app/src` - Python source code
- `./alembic` → `/app/alembic` - Database migrations
- `./templates` → `/app/templates` - Email templates
- `./scripts` → `/app/scripts` - Utility scripts

### Rebuild Actions (Container Restart)
- `./pyproject.toml` - When dependencies change

### Ignored Files
The watch ignores:
- `__pycache__/`
- `*.pyc`, `*.pyo`, `*.pyd`
- `.pytest_cache/`

## Development Workflow

### Making Code Changes

1. Edit any file in `src/`, `alembic/`, `templates/`, or `scripts/`
2. Changes are automatically synced to the container
3. FastAPI dev server auto-reloads
4. See changes immediately at http://localhost:8000

### Adding Dependencies

1. Edit `pyproject.toml`
2. The container will automatically rebuild
3. Wait for the rebuild to complete

### Viewing Logs

Check all logs:
```bash
docker compose logs
```

Check specific service logs:
```bash
docker compose logs api
docker compose logs db
docker compose logs mailcatcher
```

Follow logs in real-time:
```bash
docker compose logs -f api
```

### Database Management

Access database via Adminer:
- URL: http://localhost:8080
- System: PostgreSQL
- Server: db
- Username: From `POSTGRES_USER` in `.env`
- Password: From `POSTGRES_PASSWORD` in `.env`
- Database: From `POSTGRES_DB` in `.env`

Run migrations:
```bash
docker compose exec api uv run alembic upgrade head
```

Create new migration:
```bash
docker compose exec api uv run alembic revision --autogenerate -m "description"
```

### Email Testing

All emails sent by the API are caught by MailCatcher:
- View emails at: http://localhost:1080
- SMTP configured automatically in `docker-compose.override.yml`

## Local Development Without Docker

You can also run services locally while keeping others in Docker.

### Stop the API container:
```bash
docker compose stop api
```

### Run API locally:
```bash
# Ensure database is still running in Docker
fastapi dev src/main.py
```

The API will still connect to the Docker database on `localhost:5432`.

### Stop the database container:
```bash
docker compose stop db
```

Then configure your local PostgreSQL connection in `.env`.

## Using localhost.tiangolo.com for Subdomain Testing

To test subdomain routing locally (like production):

1. Edit `.env`:
```env
DOMAIN=localhost.tiangolo.com
```

2. Restart stack:
```bash
docker compose watch
```

3. Access services via subdomains:
- API: http://api.localhost.tiangolo.com
- Adminer: http://adminer.localhost.tiangolo.com

The domain `localhost.tiangolo.com` automatically resolves to `127.0.0.1`.

## Project Structure (FastAPI Best Practices)

```
fast-back/
├── src/                          # Main application code
│   ├── auth/                     # Authentication module
│   │   ├── router.py            # Auth endpoints
│   │   ├── schemas.py           # Pydantic models
│   │   ├── models.py            # Database models
│   │   ├── service.py           # Business logic
│   │   ├── dependencies.py      # Route dependencies
│   │   └── utils.py             # Helper functions
│   ├── items/                    # Items module
│   │   └── ...                  # Same structure
│   ├── config.py                # Global configuration
│   ├── database.py              # Database connection
│   ├── models.py                # Global models
│   ├── exceptions.py            # Global exceptions
│   ├── pagination.py            # Pagination utilities
│   └── main.py                  # FastAPI app entry
├── alembic/                      # Database migrations
├── templates/                    # Email templates
├── scripts/                      # Utility scripts
├── tests/                        # Test suite
├── docker-compose.yml           # Production config
├── docker-compose.override.yml  # Development overrides
├── Dockerfile                   # Container definition
├── pyproject.toml              # Dependencies
└── .env                        # Environment variables
```

## Troubleshooting

### Container won't start
```bash
docker compose down
docker compose build --no-cache
docker compose watch
```

### Database connection issues
Check if database is healthy:
```bash
docker compose ps
```

View database logs:
```bash
docker compose logs db
```

### Port already in use
Stop conflicting services or change ports in `docker-compose.override.yml`:
```yaml
api:
  ports:
    - "8001:80"  # Change 8000 to 8001
```

### Changes not reflecting
1. Check if watch is running: `docker compose ps`
2. Check logs: `docker compose logs -f api`
3. Restart watch: `docker compose down && docker compose watch`

### Clear everything and start fresh
```bash
docker compose down -v
docker compose build --no-cache
docker compose watch
```

## Environment Variables

Key variables in `.env`:

- `ENVIRONMENT`: local | staging | production
- `DOMAIN`: localhost (or localhost.tiangolo.com)
- `POSTGRES_*`: Database credentials
- `SECRET_KEY`: JWT secret (generate with `openssl rand -base64 32`)
- `FIRST_SUPERUSER`: Admin email
- `FIRST_SUPERUSER_PASSWORD`: Admin password

## Testing

Run tests in container:
```bash
docker compose exec api uv run pytest
```

Run tests with coverage:
```bash
docker compose exec api uv run pytest --cov=src --cov-report=html
```

## Best Practices Followed

1. **Modular Structure**: Each domain has its own directory with router, schemas, models, service
2. **Separation of Concerns**: Business logic in service.py, routes in router.py
3. **Type Safety**: Pydantic models for validation
4. **Hot Reload**: Instant feedback during development
5. **Container Isolation**: Consistent environment across team
6. **Database Migrations**: Alembic for version control
7. **Email Testing**: MailCatcher for local email debugging

## Next Steps

1. Start the stack: `docker compose watch`
2. Create your first module in `src/your_module/`
3. Add routes, schemas, models following the pattern in `src/auth/` or `src/items/`
4. Test your endpoints at http://localhost:8000/docs
5. Check emails at http://localhost:1080

Happy coding! 🚀
