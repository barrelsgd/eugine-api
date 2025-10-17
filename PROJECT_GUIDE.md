# 🚀 FastAPI Project Guide

**Last Updated**: October 14, 2025  
**Status**: ✅ Production Ready - All Systems Operational

---

## 📖 Quick Start

### First Time Setup
```bash
# 1. Setup environment
./scripts/setup.sh

# 2. Start services
docker compose up -d

# 3. Verify everything works
docker compose exec api python scripts/quick_test.py
```

### Access Your Application
- **API Documentation**: http://localhost:8000/docs
- **API (Alternative Docs)**: http://localhost:8000/redoc
- **Database UI (Adminer)**: http://localhost:8080
- **Email Testing (MailCatcher)**: http://localhost:1080
- **Traefik Dashboard**: http://localhost:8090

---

## 🎯 What's Been Implemented

### ✅ Best Practices (from zhanymkanov/fastapi-best-practices)

1. **Project Structure** - Netflix Dispatch pattern
   - Features organized by domain (`auth/`, `items/`, `utils/`)
   - Each feature has: models, schemas, service, router, dependencies

2. **Router Organization** - Single Responsibility Principle
   - Auth split into: `login.py`, `users.py`, `roles.py`, `permissions.py`
   - Clear separation of concerns

3. **Constants Management** - No magic strings
   - `src/auth/constants.py` - Auth messages
   - `src/items/constants.py` - Item messages

4. **API Documentation** - Enhanced OpenAPI
   - Detailed `responses` parameter on endpoints
   - Clear error codes and descriptions

5. **Database** - PostgreSQL naming conventions
   - Consistent index, constraint, foreign key naming
   - Applied to both SQLModel and Alembic

6. **Dependency Injection** - Proper patterns
   - Type-annotated dependencies with `Annotated`
   - Injectable settings for testability
   - Dependency chaining and composition

7. **Configuration** - Environment-based settings
   - Pydantic Settings with `.env` file
   - Different configs for local/staging/production

8. **Testing** - Automated verification
   - `quick_test.py` - 7 comprehensive tests
   - All tests passing ✅

---

## 📁 Project Structure

```
fast-back/
├── src/                          # Application code
│   ├── auth/                     # Authentication module
│   │   ├── routers/              # Split auth routers
│   │   │   ├── login.py          # Login endpoints
│   │   │   ├── users.py          # User management
│   │   │   ├── roles.py          # Role management
│   │   │   └── permissions.py    # Permission management
│   │   ├── constants.py          # Auth messages
│   │   ├── models.py             # User, Role, Permission models
│   │   ├── schemas.py            # Pydantic schemas
│   │   ├── service.py            # Business logic
│   │   └── dependencies.py       # Auth dependencies
│   ├── items/                    # Items module
│   │   ├── constants.py          # Item messages
│   │   ├── models.py             # Item model
│   │   ├── schemas.py            # Item schemas
│   │   ├── service.py            # Item business logic
│   │   └── router.py             # Item endpoints
│   ├── utils/                    # Utilities
│   │   └── router.py             # Health check, test email
│   ├── config.py                 # Settings (Pydantic)
│   ├── database.py               # DB connection, naming conventions
│   ├── dependencies.py           # Global dependencies
│   ├── email.py                  # Email functionality
│   ├── main.py                   # FastAPI app
│   └── pagination.py             # Pagination helpers
│
├── tests/                        # Test suite
│   ├── api/routes/               # API endpoint tests
│   ├── crud/                     # CRUD operation tests
│   └── conftest.py               # Test fixtures
│
├── scripts/                      # Development scripts
│   ├── dev.sh                    # Main development tool ⭐
│   ├── setup.sh                  # First-time setup
│   ├── db.sh                     # Database management
│   ├── format.sh                 # Code formatting
│   ├── lint.sh                   # Code quality checks
│   ├── test.sh                   # Run test suite
│   ├── quick_test.py             # Fast API tests
│   ├── seed_data.py              # Test data generation
│   ├── clean.sh                  # Cleanup artifacts
│   ├── pre-deploy.sh             # Pre-deployment checks
│   ├── backend_pre_start.py      # DB health check
│   ├── initial_data.py           # Create superuser
│   ├── prestart.sh               # Container startup
│   └── README.md                 # Scripts documentation
│
├── email-templates/              # Email templates
│   ├── src/                      # MJML sources (editable)
│   │   ├── new_account.mjml
│   │   ├── reset_password.mjml
│   │   └── test_email.mjml
│   ├── build/                    # HTML outputs (used by app)
│   │   ├── new_account.html
│   │   ├── reset_password.html
│   │   └── test_email.html
│   └── README.md                 # Email template docs
│
├── alembic/                      # Database migrations
│   ├── versions/                 # Migration files (date-based naming)
│   └── env.py                    # Alembic config
│
├── docker-compose.yml            # Main Docker config
├── docker-compose.override.yml   # Local dev overrides
├── Dockerfile                    # Container definition
├── pyproject.toml                # Python dependencies (uv)
├── .env                          # Environment variables
├── README.md                     # Project overview
├── QUICKSTART.md                 # Quick start guide
├── DEVELOPMENT.md                # Development guide
├── DEPLOYMENT.md                 # Deployment guide
└── TESTING.md                    # Testing guide
```

---

## 🛠️ Common Commands

### Development Workflow

```bash
# Start development
./scripts/dev.sh start

# View logs
./scripts/dev.sh logs-api

# Open shell in container
./scripts/dev.sh shell

# Code quality
./scripts/format.sh              # Format code
./scripts/lint.sh                # Check quality

# Testing
./scripts/dev.sh test-cov        # Run tests with coverage
docker compose exec api python scripts/quick_test.py  # Quick API test

# Stop services
./scripts/dev.sh stop
```

### Database Management

```bash
# Database operations
./scripts/db.sh shell            # Open PostgreSQL shell
./scripts/db.sh backup           # Create backup
./scripts/db.sh migrate          # Apply migrations
./scripts/db.sh migration "msg"  # Create new migration
./scripts/db.sh seed             # Add test data
./scripts/db.sh reset            # Reset database (⚠️ deletes data)
```

### Maintenance

```bash
# Cleanup
./scripts/clean.sh               # Remove cache files

# Pre-deployment checks
./scripts/pre-deploy.sh          # Validate before deploying

# View status
./scripts/dev.sh status          # Check container status
```

---

## 🔑 Key Features

### Authentication System
- ✅ JWT-based authentication
- ✅ Role-based access control (RBAC)
- ✅ User registration and management
- ✅ Password reset functionality
- ✅ Email verification support

### API Features
- ✅ Auto-generated OpenAPI documentation
- ✅ Enhanced API docs with response codes
- ✅ Standardized pagination
- ✅ Consistent error handling
- ✅ CORS support

### Database
- ✅ PostgreSQL with SQLModel
- ✅ Alembic migrations (date-based naming)
- ✅ Database naming conventions
- ✅ Relationship management with cascade deletes

### Email System
- ✅ SMTP support (MailCatcher for local dev)
- ✅ Resend API support (for production)
- ✅ MJML responsive email templates
- ✅ Welcome emails, password resets, test emails

### Development Tools
- ✅ Docker Compose for local development
- ✅ Hot reload with watch mode
- ✅ Comprehensive development scripts
- ✅ Automated testing
- ✅ Code formatting (Ruff)
- ✅ Type checking (mypy)
- ✅ Linting (Ruff)

---

## 📚 Documentation

### Core Documentation
- **README.md** - Project overview and setup
- **QUICKSTART.md** - Get started in 5 minutes
- **DEVELOPMENT.md** - Detailed development guide
- **DEPLOYMENT.md** - Production deployment guide
- **TESTING.md** - Testing strategies and guides

### Feature Documentation
- **scripts/README.md** - All development scripts
- **email-templates/README.md** - Email template editing

---

## 🧪 Testing

### Quick API Test
```bash
docker compose exec api python scripts/quick_test.py
```

**Tests:**
1. ✅ API Health Check
2. ✅ Router Structure (6 tag groups)
3. ✅ Enhanced Documentation
4. ✅ User Registration
5. ✅ Login Flow
6. ✅ Authenticated Endpoints
7. ✅ Constants Usage

### Full Test Suite
```bash
./scripts/dev.sh test-cov
```

Generates coverage report in `htmlcov/index.html`

---

## 🚀 Deployment

### Pre-Deployment Checklist
```bash
./scripts/pre-deploy.sh
```

**Validates:**
- Environment variables
- Code formatting
- Linting
- Type checking
- Database migrations
- Tests
- API health
- Security issues
- Docker build
- Dependencies

### Production Deployment
See `DEPLOYMENT.md` for detailed instructions.

---

## 🔧 Configuration

### Environment Variables

**Required:**
```env
SECRET_KEY=your-secret-key
POSTGRES_PASSWORD=your-db-password
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=your-admin-password
```

**Email (Production):**
```env
RESEND_API_KEY=your-resend-api-key
EMAILS_FROM_EMAIL=noreply@yourdomain.com
```

**Optional:**
```env
FRONTEND_HOST=https://yourfrontend.com
SENTRY_DSN=your-sentry-dsn
```

See `.env.example` for all options.

---

## 🎓 Learning Resources

### Your Project
1. **Start with**: `QUICKSTART.md`
2. **Understand structure**: Explore `src/` directory
3. **Try scripts**: Use `./scripts/dev.sh` commands
4. **Read docs**: Check `scripts/README.md`

### External Resources
- **FastAPI Best Practices**: https://github.com/zhanymkanov/fastapi-best-practices
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **SQLModel Docs**: https://sqlmodel.tiangolo.com
- **Pydantic Docs**: https://docs.pydantic.dev

---

## 🎯 Next Steps (Optional)

### Performance
- [ ] Add Redis caching
- [ ] Implement rate limiting
- [ ] Move to async database operations
- [ ] Add database connection pooling

### Features
- [ ] WebSocket support
- [ ] Background tasks with Celery
- [ ] File upload handling
- [ ] Admin dashboard

### DevOps
- [x] Set up CI/CD (GitHub Actions) ✅
- [ ] Add monitoring (Prometheus/Grafana)
- [ ] Implement logging (ELK stack)
- [x] Add health checks for all dependencies ✅

### Quality
- [ ] Increase test coverage
- [ ] Add integration tests
- [ ] Add performance tests
- [ ] Set up pre-commit hooks

---

## 💡 Tips & Best Practices

### Daily Development
1. Always start with `./scripts/dev.sh start`
2. Run `./scripts/format.sh` before committing
3. Check `./scripts/lint.sh` for code quality
4. Use `./scripts/quick_test.py` after changes

### Database Changes
1. Make model changes in `src/*/models.py`
2. Create migration: `./scripts/db.sh migration "description"`
3. Review migration in `alembic/versions/`
4. Apply: `./scripts/db.sh migrate`

### Email Templates
1. Edit `.mjml` files in `email-templates/src/`
2. Build to HTML with `mjml` command
3. Test with `/api/v1/utils/test-email`
4. Check MailCatcher at http://localhost:1080

### Before Deploying
1. Run `./scripts/pre-deploy.sh`
2. Fix any failures
3. Create database backup
4. Deploy with confidence!

---

## 🆘 Troubleshooting

### Containers Won't Start
```bash
docker compose down -v
docker compose build --no-cache
docker compose up -d
```

### Database Connection Issues
```bash
docker compose restart db
# Wait a few seconds
docker compose up -d
```

### Tests Failing
```bash
./scripts/dev.sh logs-api        # Check logs
./scripts/db.sh reset            # Reset database if needed
./scripts/db.sh seed             # Add test data
```

### Email Not Sending
```bash
# Check MailCatcher is running
docker compose ps

# View email service logs
./scripts/dev.sh logs-api | grep EMAIL
```

### Import Errors
```bash
# Reinstall dependencies
docker compose exec api uv sync
```

---

## 📊 Project Status

| Component | Status | Notes |
|-----------|--------|-------|
| **Core API** | ✅ Complete | All endpoints working |
| **Authentication** | ✅ Complete | JWT, RBAC, roles |
| **Database** | ✅ Complete | PostgreSQL with migrations |
| **Email System** | ✅ Complete | SMTP + Resend support |
| **Testing** | ✅ Complete | 7/7 tests passing |
| **Documentation** | ✅ Complete | Comprehensive guides |
| **Scripts** | ✅ Complete | 10 development scripts |
| **Docker Setup** | ✅ Complete | Local + production configs |
| **Code Quality** | ✅ Complete | Formatting, linting, typing |

---

## 🎉 Summary

Your FastAPI project is:
- ✅ **Well-structured** - Netflix Dispatch pattern
- ✅ **Best practices** - Following industry standards
- ✅ **Fully documented** - Comprehensive guides
- ✅ **Production-ready** - Docker, migrations, testing
- ✅ **Developer-friendly** - Great DX with scripts
- ✅ **Maintainable** - Clean code, constants, typing

**You're ready to build amazing things!** 🚀

---

**Questions?** Check the documentation or explore the code!

**Last Updated**: October 14, 2025  
**Version**: 1.0.0

