# 🌐 Application URLs

Complete reference for all application URLs in different environments.

---

## 🏠 Development URLs (localhost)

**For local development with standard localhost addresses.**

### Backend API
- **Base URL**: http://localhost:8000
- **Swagger UI (Interactive Docs)**: http://localhost:8000/docs
- **ReDoc (Alternative Docs)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/utils/health-check/

### Development Tools
- **Adminer (Database UI)**: http://localhost:8080
- **Traefik Dashboard**: http://localhost:8090
- **MailCatcher (Email Testing)**: http://localhost:1080

### Direct Database Access
- **PostgreSQL**: `localhost:5432`
  - Username: `app` (default)
  - Password: From `.env` file
  - Database: `app` (default)

---

## 🌍 Development URLs with Custom Domain

**For local development using `localhost.tiangolo.com` (requires Traefik routing).**

### Backend API
- **Base URL**: http://api.localhost.tiangolo.com
- **Swagger UI**: http://api.localhost.tiangolo.com/docs
- **ReDoc**: http://api.localhost.tiangolo.com/redoc

### Development Tools
- **Adminer**: http://adminer.localhost.tiangolo.com
- **Traefik Dashboard**: http://localhost.tiangolo.com:8090
- **MailCatcher**: http://localhost.tiangolo.com:1080

### Setup for Custom Domain
To use custom domain URLs, configure your Traefik labels in `docker-compose.yml`:

```yaml
environment:
  - DOMAIN=localhost.tiangolo.com
```

---

## 🚀 Production/Staging URLs

**Replace `yourdomain.com` with your actual domain.**

### Backend API
- **Base URL**: https://api.yourdomain.com
- **Swagger UI**: https://api.yourdomain.com/docs (if enabled)
- **ReDoc**: https://api.yourdomain.com/redoc (if enabled)
- **Health Check**: https://api.yourdomain.com/api/v1/utils/health-check/

### Database Management
- **Adminer**: https://adminer.yourdomain.com (configure in Traefik)

**Note**: API docs (Swagger/ReDoc) are automatically disabled in production for security.

---

## 📋 Quick Reference Table

### Development (localhost)

| Service | URL | Purpose |
|---------|-----|---------|
| **API** | http://localhost:8000 | Backend API |
| **Swagger Docs** | http://localhost:8000/docs | Interactive API documentation |
| **ReDoc** | http://localhost:8000/redoc | Alternative API documentation |
| **Adminer** | http://localhost:8080 | Database management UI |
| **Traefik** | http://localhost:8090 | Reverse proxy dashboard |
| **MailCatcher** | http://localhost:1080 | Email testing interface |
| **PostgreSQL** | localhost:5432 | Direct database connection |

### Development (with Traefik routing)

| Service | URL | Purpose |
|---------|-----|---------|
| **API** | http://api.localhost.tiangolo.com | Backend API via Traefik |
| **Swagger Docs** | http://api.localhost.tiangolo.com/docs | Interactive docs via Traefik |
| **ReDoc** | http://api.localhost.tiangolo.com/redoc | Alternative docs via Traefik |
| **Adminer** | http://adminer.localhost.tiangolo.com | Database UI via Traefik |
| **Traefik** | http://localhost.tiangolo.com:8090 | Traefik dashboard |
| **MailCatcher** | http://localhost.tiangolo.com:1080 | Email testing |

---

## 🔧 Testing URLs

### Quick Health Check
```bash
# Test API is running
curl http://localhost:8000/api/v1/utils/health-check/

# Should return: true
```

### Test Email System
```bash
# Send test email
curl -X POST "http://localhost:8000/api/v1/utils/test-email?email_to=test@example.com" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Check email at:
open http://localhost:1080
```

### Test Authentication
```bash
# Login
curl -X POST "http://localhost:8000/api/v1/login/access-token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=changethis"

# Returns JWT token
```

---

## 🛠️ Configuration

### Environment Variables

Set these in your `.env` file:

```env
# Domain (for Traefik routing)
DOMAIN=localhost

# Or for custom local domain:
DOMAIN=localhost.tiangolo.com

# Frontend (for CORS and password reset links)
FRONTEND_HOST=http://localhost:3000
```

### Traefik Configuration

The Traefik configuration is in `docker-compose.yml`:

```yaml
labels:
  # API routing
  - traefik.http.routers.fast-back-api-http.rule=Host(`${DOMAIN:-localhost}`) && (PathPrefix(`/api`) || PathPrefix(`/docs`) || PathPrefix(`/redoc`))
  
  # Adminer routing
  - traefik.http.routers.fast-back-adminer-http.rule=Host(`adminer.${DOMAIN:-localhost}`)
```

---

## 📱 Access from Different Devices

### Same Network
To access from other devices on your local network:

1. Find your local IP:
   ```bash
   # Mac/Linux
   ifconfig | grep "inet "
   
   # Windows
   ipconfig
   ```

2. Use your IP instead of localhost:
   - http://192.168.1.100:8000 (replace with your IP)

3. Update CORS in `.env`:
   ```env
   BACKEND_CORS_ORIGINS=["http://192.168.1.100:3000","http://localhost:3000"]
   ```

### Using ngrok (Public Testing)
```bash
# Expose local API to internet
ngrok http 8000

# Use the generated URL (e.g., https://abc123.ngrok.io)
```

---

## 🔒 Security Notes

### Development
- ✅ API docs are enabled
- ✅ CORS is permissive
- ✅ Default passwords are acceptable
- ✅ HTTP (not HTTPS) is fine

### Production
- ❌ API docs are disabled (security)
- ❌ CORS is restrictive (configured domains only)
- ❌ Strong passwords required
- ❌ HTTPS only (with valid certificate)

---

## 🎯 Common Tasks

### Opening URLs in Browser

**Mac/Linux:**
```bash
open http://localhost:8000/docs
```

**Windows:**
```bash
start http://localhost:8000/docs
```

### Testing All Services
```bash
# Run quick test
docker compose exec api python scripts/quick_test.py

# Should show all services working
```

### Viewing Logs
```bash
# API logs
docker compose logs -f api

# All services
docker compose logs -f
```

---

## 🆘 Troubleshooting

### Port Already in Use

**Error**: `Bind for 0.0.0.0:8000 failed: port is already allocated`

**Solution**:
```bash
# Find what's using the port
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process or stop the service
# Then restart Docker Compose
docker compose down
docker compose up -d
```

### Can't Access URL

**Check services are running:**
```bash
docker compose ps
```

**Restart services:**
```bash
docker compose restart
```

**Check logs:**
```bash
docker compose logs api
```

### Database Connection Failed

**Check database is healthy:**
```bash
docker compose ps db
# Should show "healthy"
```

**Restart database:**
```bash
docker compose restart db
```

---

## 📚 Related Documentation

- **QUICKSTART.md** - Quick setup guide
- **DEVELOPMENT.md** - Development workflow
- **DEPLOYMENT.md** - Production deployment
- **scripts/README.md** - Development scripts

---

## ✅ Verification Checklist

After starting services, verify all URLs work:

- [ ] API: http://localhost:8000/api/v1/utils/health-check/
- [ ] Swagger: http://localhost:8000/docs
- [ ] ReDoc: http://localhost:8000/redoc
- [ ] Adminer: http://localhost:8080
- [ ] Traefik: http://localhost:8090
- [ ] MailCatcher: http://localhost:1080

**All should be accessible!** ✅

---

**Last Updated**: October 14, 2025  
**Status**: ✅ All URLs Configured

