# Docker & Environment Configuration Guide

This guide explains the Docker and environment configuration for the FastAPI project, following best practices for deployment.

## 📁 Environment Files

### Environment File Structure
```
├── .env.local.example      # Local development template
├── .env.staging.example    # Staging environment template  
├── .env.production.example # Production environment template
└── .env.local              # Your local development file (create from example)
```

### Environment File Usage

#### Local Development
```bash
# Copy the local example file
cp .env.local.example .env.local

# Edit with your local settings
nano .env.local
```

#### Staging Deployment
```bash
# Copy the staging example file
cp .env.staging.example .env.staging

# Edit with your staging settings
nano .env.staging
```

#### Production Deployment
```bash
# Copy the production example file
cp .env.production.example .env.production

# Edit with your production settings
nano .env.production
```

## 🐳 Docker Configuration

### Docker Files Overview
```
├── Dockerfile              # Development Docker image
├── Dockerfile.prod         # Production Docker image (multi-stage)
├── docker-compose.yml      # Base services configuration
├── docker-compose.override.yml  # Local development overrides
├── docker-compose.staging.yml   # Staging deployment
├── docker-compose.prod.yml      # Production deployment
└── docker-compose.traefik.yml   # Traefik reverse proxy
```

### Docker Compose Environments

#### Local Development
```bash
# Start local development environment
docker compose up -d

# This uses:
# - docker-compose.yml (base services)
# - docker-compose.override.yml (development overrides)
# - .env.local (local environment variables)
```

#### Staging Deployment
```bash
# Deploy to staging
docker compose -f docker-compose.staging.yml --env-file .env.staging up -d

# This uses:
# - docker-compose.staging.yml (staging configuration)
# - .env.staging (staging environment variables)
```

#### Production Deployment
```bash
# Deploy to production
docker compose -f docker-compose.prod.yml --env-file .env.production up -d

# This uses:
# - docker-compose.prod.yml (production configuration)
# - .env.production (production environment variables)
```

## 🔧 Key Configuration Features

### Security Best Practices
- ✅ **Non-root user**: All containers run as non-root user (`appuser`)
- ✅ **Health checks**: Proper health checks for all services
- ✅ **Environment separation**: Different configs for each environment
- ✅ **Secret management**: Environment variables for sensitive data
- ✅ **Multi-stage builds**: Optimized production images

### Production Features
- ✅ **Traefik integration**: Automatic HTTPS with Let's Encrypt
- ✅ **Service dependencies**: Proper startup order with health checks
- ✅ **Restart policies**: Automatic restart on failure
- ✅ **Volume persistence**: Database data persistence
- ✅ **Network isolation**: Secure network configuration

### Development Features
- ✅ **Hot reload**: Automatic code reloading in development
- ✅ **Volume mounts**: Live code editing without rebuilds
- ✅ **MailCatcher**: Local email testing
- ✅ **Adminer**: Database management interface
- ✅ **Debug mode**: Enhanced logging and debugging

## 🚀 Deployment Workflow

### 1. Local Development
```bash
# Start development environment
docker compose up -d

# View logs
docker compose logs -f api

# Run tests
docker compose exec api python scripts/quick_test.py
```

### 2. Staging Deployment
```bash
# Build and push staging image
docker build -f Dockerfile.prod -t ghcr.io/your-org/fast-back:staging .
docker push ghcr.io/your-org/fast-back:staging

# Deploy to staging
docker compose -f docker-compose.staging.yml --env-file .env.staging up -d
```

### 3. Production Deployment
```bash
# Build and push production image
docker build -f Dockerfile.prod -t ghcr.io/your-org/fast-back:latest .
docker push ghcr.io/your-org/fast-back:latest

# Deploy to production
docker compose -f docker-compose.prod.yml --env-file .env.production up -d
```

## 🔍 Environment Variables Reference

### Core Configuration
- `ENVIRONMENT`: Environment name (local/staging/production)
- `PROJECT_NAME`: Project display name
- `STACK_NAME`: Docker stack name
- `DOMAIN`: Primary domain
- `FRONTEND_HOST`: Frontend application URL

### Security
- `SECRET_KEY`: JWT secret key (CRITICAL - change in production!)
- `POSTGRES_PASSWORD`: Database password (CRITICAL - change in production!)
- `FIRST_SUPERUSER_PASSWORD`: Admin password (CRITICAL - change in production!)

### Database
- `POSTGRES_SERVER`: Database host
- `POSTGRES_PORT`: Database port
- `POSTGRES_DB`: Database name
- `POSTGRES_USER`: Database user

### Email
- `RESEND_API_KEY`: Resend API key for production emails
- `SMTP_HOST`: SMTP server host
- `SMTP_PORT`: SMTP server port
- `SMTP_TLS`: Enable TLS
- `EMAILS_FROM_EMAIL`: From email address
- `EMAILS_FROM_NAME`: From name

### Monitoring
- `SENTRY_DSN`: Sentry error tracking DSN
- `BACKEND_CORS_ORIGINS`: Allowed CORS origins

## 🛠️ Troubleshooting

### Common Issues

#### Container Won't Start
```bash
# Check logs
docker compose logs api

# Check environment variables
docker compose exec api env | grep POSTGRES
```

#### Database Connection Issues
```bash
# Check database health
docker compose exec db pg_isready -U app -d app

# Check database logs
docker compose logs db
```

#### Health Check Failures
```bash
# Test health check manually
curl http://localhost:8000/api/v1/utils/health-check/

# Check health check logs
docker compose exec api python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/utils/health-check/').read()"
```

### Environment Variable Issues
```bash
# Verify environment file is loaded
docker compose exec api env | grep ENVIRONMENT

# Check for missing variables
docker compose config
```

## 📋 Best Practices Checklist

### Before Deployment
- [ ] All environment files created and configured
- [ ] Secret keys changed from defaults
- [ ] Database passwords are secure
- [ ] CORS origins are properly configured
- [ ] Email configuration is working
- [ ] Health checks are passing
- [ ] SSL certificates are configured (production)

### Security Checklist
- [ ] Non-root user in containers
- [ ] Environment variables for secrets
- [ ] HTTPS enabled (production)
- [ ] Database access restricted
- [ ] CORS properly configured
- [ ] Error tracking configured

### Performance Checklist
- [ ] Multi-stage Docker builds
- [ ] Health checks configured
- [ ] Restart policies set
- [ ] Volume persistence configured
- [ ] Network optimization
- [ ] Resource limits set (if needed)

## 🔗 Related Documentation

- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- [GITHUB_SECRETS.md](GITHUB_SECRETS.md) - GitHub secrets configuration
- [URLS.md](URLS.md) - Service URLs and access
- [PROJECT_GUIDE.md](PROJECT_GUIDE.md) - Overall project guide

## 📞 Support

If you encounter issues with Docker or environment configuration:

1. Check the logs: `docker compose logs -f`
2. Verify environment variables: `docker compose config`
3. Test health checks: `curl http://localhost:8000/api/v1/utils/health-check/`
4. Review this guide and related documentation
5. Check GitHub Issues for known problems
