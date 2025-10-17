# FastAPI Backend - Barrels API

A modern FastAPI backend following [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices) with [FastAPI Full-Stack Template](https://github.com/fastapi/full-stack-fastapi-template) development workflow.

## Features

- ✅ **FastAPI Best Practices Structure**: Modular architecture with `src/` directory
- ✅ **Docker Compose Watch**: Hot-reload for instant development feedback
- ✅ **Type Safety**: Full Pydantic validation and type hints
- ✅ **Database Migrations**: Alembic for version control
- ✅ **Authentication**: JWT-based auth with secure password hashing
- ✅ **Email Testing**: MailCatcher for local email debugging
- ✅ **API Documentation**: Auto-generated Swagger UI and ReDoc
- ✅ **Database UI**: Adminer for easy database management
- ✅ **Traefik Proxy**: Production-like routing in development

## Quick Start

### Prerequisites

- Docker Desktop (with Docker Compose v2.22+)
- Git

### Setup

1. **Clone and navigate to project**:
```bash
cd fast-back
```

2. **Copy environment file**:
```bash
cp .env.example .env
```

3. **Edit `.env` and set secure values**:
```env
SECRET_KEY=your-secret-key-here  # Generate with: openssl rand -base64 32
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=your-secure-password
POSTGRES_PASSWORD=your-db-password
```

4. **Start development environment**:
```bash
docker compose watch
```

Or use the helper script:
```bash
# Windows PowerShell
.\scripts\dev.ps1 start

# Linux/Mac
./scripts/dev.sh start
```

5. **Access your services**:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Adminer: http://localhost:8080
- MailCatcher: http://localhost:1080
- Traefik: http://localhost:8090

## Development Workflow

### Making Changes

Edit any file in `src/`, `alembic/`, `templates/`, or `scripts/` - changes sync automatically and the server reloads instantly.

### Helper Scripts

**Windows (PowerShell)**:
```powershell
.\scripts\dev.ps1 start        # Start with watch mode
.\scripts\dev.ps1 logs-api     # View API logs
.\scripts\dev.ps1 shell        # Open container shell
.\scripts\dev.ps1 migrate      # Run migrations
.\scripts\dev.ps1 test         # Run tests
.\scripts\dev.ps1 help         # Show all commands
```

**Linux/Mac (Bash)**:
```bash
./scripts/dev.sh start         # Start with watch mode
./scripts/dev.sh logs-api      # View API logs
./scripts/dev.sh shell         # Open container shell
./scripts/dev.sh migrate       # Run migrations
./scripts/dev.sh test          # Run tests
./scripts/dev.sh help          # Show all commands
```

### Database Migrations

Create a new migration:
```bash
docker compose exec api uv run alembic revision --autogenerate -m "add users table"
```

Apply migrations:
```bash
docker compose exec api uv run alembic upgrade head
```

### Running Tests

```bash
docker compose exec api uv run pytest
```

With coverage:
```bash
docker compose exec api uv run pytest --cov=src --cov-report=html
```

## Project Structure

```
fast-back/
├── src/                          # Application code
│   ├── auth/                     # Authentication module
│   │   ├── router.py            # Auth endpoints
│   │   ├── schemas.py           # Pydantic models
│   │   ├── models.py            # Database models
│   │   ├── service.py           # Business logic
│   │   ├── dependencies.py      # Route dependencies
│   │   └── utils.py             # Helper functions
│   ├── items/                    # Items module (example)
│   ├── config.py                # Global configuration
│   ├── database.py              # Database connection
│   ├── models.py                # Global models
│   ├── exceptions.py            # Global exceptions
│   └── main.py                  # FastAPI app entry
├── alembic/                      # Database migrations
├── templates/                    # Email templates
├── scripts/                      # Utility scripts
│   ├── dev.ps1                  # Windows helper
│   └── dev.sh                   # Linux/Mac helper
├── tests/                        # Test suite
├── docker-compose.yml           # Production config
├── docker-compose.override.yml  # Development overrides
├── Dockerfile                   # Container definition
├── pyproject.toml              # Dependencies (uv)
├── .env                        # Environment variables
└── DEVELOPMENT.md              # Detailed dev guide
```

## Architecture

This project follows **FastAPI Best Practices**:

1. **Modular Structure**: Each domain (auth, items, etc.) has its own directory
2. **Separation of Concerns**:
   - `router.py`: API endpoints
   - `schemas.py`: Request/response models
   - `models.py`: Database models
   - `service.py`: Business logic
   - `dependencies.py`: Dependency injection
   - `utils.py`: Helper functions
3. **Type Safety**: Pydantic models everywhere
4. **Async/Await**: Non-blocking I/O operations
5. **Dependency Injection**: FastAPI's DI system

## Docker Compose Watch

The project uses Docker Compose watch mode for development:

- **Sync**: Changes to Python files sync instantly
- **Rebuild**: Changes to `pyproject.toml` trigger rebuild
- **Ignore**: `__pycache__`, `.pyc` files ignored
- **Hot Reload**: FastAPI dev server auto-reloads

## Environment Variables

Key variables in `.env`:

| Variable | Description | Example |
|----------|-------------|---------|
| `ENVIRONMENT` | Environment name | `local`, `staging`, `production` |
| `DOMAIN` | Base domain | `localhost` or `localhost.tiangolo.com` |
| `SECRET_KEY` | JWT secret | Generate with `openssl rand -base64 32` |
| `POSTGRES_*` | Database credentials | See `.env.example` |
| `FIRST_SUPERUSER` | Admin email | `admin@example.com` |
| `FIRST_SUPERUSER_PASSWORD` | Admin password | Strong password |

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing Emails

All emails are caught by MailCatcher:
- **Web UI**: http://localhost:1080
- **SMTP**: `mailcatcher:1025` (configured automatically)

## Database Management

Access Adminer at http://localhost:8080:
- **System**: PostgreSQL
- **Server**: db
- **Username**: From `POSTGRES_USER` in `.env`
- **Password**: From `POSTGRES_PASSWORD` in `.env`
- **Database**: From `POSTGRES_DB` in `.env`

## Troubleshooting

### Port conflicts
Change ports in `docker-compose.override.yml`:
```yaml
api:
  ports:
    - "8001:80"  # Change 8000 to 8001
```

### Container won't start
```bash
docker compose down
docker compose build --no-cache
docker compose watch
```

### Changes not reflecting
```bash
docker compose logs -f api  # Check for errors
docker compose restart api   # Restart API service
```

### Clear everything
```bash
docker compose down -v
docker compose build --no-cache
docker compose watch
```

## Documentation

- **[DEVELOPMENT.md](DEVELOPMENT.md)**: Detailed development guide
- **[FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)**: Structure guidelines
- **[FastAPI Full-Stack Template](https://github.com/fastapi/full-stack-fastapi-template)**: Development workflow

## Tech Stack

- **FastAPI**: Modern Python web framework
- **PostgreSQL**: Database
- **SQLAlchemy**: ORM
- **Alembic**: Database migrations
- **Pydantic**: Data validation
- **uv**: Fast Python package manager
- **Docker**: Containerization
- **Traefik**: Reverse proxy
- **pytest**: Testing framework

## License

[Your License Here]

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests: `docker compose exec api uv run pytest`
4. Submit a pull request

---

**Happy coding!** 🚀

For detailed development instructions, see [DEVELOPMENT.md](DEVELOPMENT.md).
