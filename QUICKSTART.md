# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Configure Environment
```bash
cp .env.example .env
```

Edit `.env` and set:
```env
SECRET_KEY=<generate-with-openssl-rand-base64-32>
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=<your-password>
POSTGRES_PASSWORD=<your-db-password>
```

### 2. Start Development
```bash
docker compose watch
```

### 3. Access Services
- 🌐 **API**: http://localhost:8000
- 📚 **Docs**: http://localhost:8000/docs
- 🗄️ **Database UI**: http://localhost:8080
- 📧 **Email Testing**: http://localhost:1080

## 📝 Common Commands

### Windows (PowerShell)
```powershell
.\scripts\dev.ps1 start        # Start with watch
.\scripts\dev.ps1 logs-api     # View logs
.\scripts\dev.ps1 shell        # Open shell
.\scripts\dev.ps1 migrate      # Run migrations
.\scripts\dev.ps1 test         # Run tests
```

### Linux/Mac (Bash)
```bash
./scripts/dev.sh start         # Start with watch
./scripts/dev.sh logs-api      # View logs
./scripts/dev.sh shell         # Open shell
./scripts/dev.sh migrate       # Run migrations
./scripts/dev.sh test          # Run tests
```

## 🔄 Development Workflow

1. **Edit code** in `src/` → Changes sync automatically
2. **See changes** instantly at http://localhost:8000
3. **Check logs**: `docker compose logs -f api`
4. **Test emails**: http://localhost:1080

## 🛠️ Database Operations

**Create migration**:
```bash
docker compose exec api uv run alembic revision --autogenerate -m "description"
```

**Apply migrations**:
```bash
docker compose exec api uv run alembic upgrade head
```

**Access database**:
- UI: http://localhost:8080
- CLI: `docker compose exec db psql -U app -d app`

## 🧪 Testing

**Run tests**:
```bash
docker compose exec api uv run pytest
```

**With coverage**:
```bash
docker compose exec api uv run pytest --cov=src --cov-report=html
```

## 🐛 Troubleshooting

**Container won't start**:
```bash
docker compose down
docker compose build --no-cache
docker compose watch
```

**Changes not reflecting**:
```bash
docker compose restart api
```

**Clear everything**:
```bash
docker compose down -v
docker compose build --no-cache
docker compose watch
```

## 📖 More Information

- **Detailed Guide**: [DEVELOPMENT.md](DEVELOPMENT.md)
- **Full README**: [README.md](README.md)
- **Best Practices**: https://github.com/zhanymkanov/fastapi-best-practices
- **Template Reference**: https://github.com/fastapi/full-stack-fastapi-template

---

**Need help?** Check [DEVELOPMENT.md](DEVELOPMENT.md) for detailed instructions.
