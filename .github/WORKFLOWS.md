# GitHub Actions Workflows

Complete reference for all GitHub Actions workflows in this project.

---

## 📋 Workflow Overview

| Workflow | Trigger | Purpose | Status |
|----------|---------|---------|--------|
| **ci.yml** | Push/PR | Code quality & testing | ✅ Active |
| **test-docker-compose.yml** | Push/PR | Docker integration test | ✅ Active |
| **deploy-production.yml** | Release | Deploy to barrels.gd | ✅ Active |
| **deploy-staging.yml** | Push to master | Deploy to staging | ✅ Active |
| **generate-client.yml** | Various | Generate frontend client | ✅ Active |
| **playwright.yml** | Push/PR | E2E tests | ✅ Active |
| **smokeshow.yml** | Various | Coverage display | ✅ Active |
| **latest-changes.yml** | Various | Changelog generation | ✅ Active |
| **issue-manager.yml** | Issues | Issue automation | ✅ Active |
| **add-to-project.yml** | Issues | Project board | ✅ Active |
| **labeler.yml** | PR | Auto-labeling | ✅ Active |

---

## 🔄 CI/CD Pipeline

### Development Flow

```
┌──────────────┐
│ Push to PR   │
└──────┬───────┘
       │
       ├─────► CI Workflow
       │       ├─ Code Quality (Ruff, mypy)
       │       ├─ Security Scan (Trivy)
       │       ├─ Tests (pytest + PostgreSQL)
       │       ├─ Docker Build Test
       │       └─ API Docs Generation
       │
       └─────► test-docker-compose
               └─ Full Docker Compose test

```

### Staging Deployment

```
┌──────────────────┐
│ Push to master   │
└────────┬─────────┘
         │
         ├─────► Wait for CI ✓
         │
         └─────► deploy-staging
                 ├─ Build Docker image
                 ├─ Deploy to staging.api.barrels.gd
                 └─ Health check
```

### Production Deployment

```
┌─────────────────┐
│ Create Release  │
└────────┬────────┘
         │
         ├─────► Wait for CI ✓
         │
         └─────► deploy-production
                 ├─ Build Docker image
                 ├─ Deploy to api.barrels.gd
                 └─ Health check
```

---

## 🎯 Workflow Details

### 1. CI Workflow (`ci.yml`)

**Purpose**: Continuous Integration - Quality & Testing

**Triggers:**
- Push to: `main`, `master`, `develop`, `dispatch`
- Pull requests to: `main`, `master`, `develop`

**Jobs:**

#### Code Quality
- Ruff linting (`ruff check`)
- Ruff formatting (`ruff format --check`)
- Type checking (`mypy`)

#### Security
- Trivy vulnerability scanning
- Uploads results to GitHub Security tab

#### Tests
- Runs with PostgreSQL service
- Full test suite with pytest
- Coverage report generation
- Codecov integration

#### Docker Build
- Tests production Dockerfile build
- Uses BuildKit caching

#### API Documentation
- Generates OpenAPI schema
- Uploads as artifact

**Environment:** Ubuntu latest  
**Python Version:** 3.11  
**Dependencies:** Managed with `uv`

### 2. Test Docker Compose (`test-docker-compose.yml`)

**Purpose**: Verify full Docker Compose stack

**Triggers:**
- Push to `master`
- Pull requests

**Steps:**
1. Prepares `.env` from `env.example`
2. Creates traefik network
3. Builds Docker Compose
4. Starts `api` and `adminer` services
5. Tests health check endpoint
6. Tears down stack

**Why it's important:** Catches Docker-specific issues

### 3. Deploy to Production (`deploy-production.yml`)

**Purpose**: Deploy releases to api.barrels.gd

**Triggers:**
- Release published (tags like `v1.0.0`)

**Requirements:**
- Self-hosted runner with label: `production`
- All CI checks must pass (`CI`, `test-docker-compose`)

**Deployment Process:**
1. **Verify Checks** - Waits for all CI jobs
2. **Setup Environment** - Loads production config from `/home/github/.config/eugine-api/production.env`
3. **Security Guards** - Validates secrets aren't default values
4. **Build** - Builds Docker images with project name `barrels-api`
5. **Deploy** - Deploys with Docker Compose
6. **Health Check** - Verifies API responds at `https://api.barrels.gd`

**Safety Features:**
- Guards against default passwords
- Retires legacy eugine-api stack
- Sanitizes logs (hides secrets)
- Extensive error logging on failure

### 4. Deploy to Staging (`deploy-staging.yml`)

**Purpose**: Auto-deploy master branch to staging

**Triggers:**
- Push to `master` branch

**Requirements:**
- Self-hosted runner with labels: `self-hosted`, `staging`
- All CI checks must pass

**Deployment Process:**
1. Verifies CI checks passed
2. Loads staging config from `/home/github/.config/eugine-api/staging.env`
3. Auto-generates strong secrets on first provision
4. Validates configuration
5. Builds and deploys to `staging.api.barrels.gd`

**Key Features:**
- Auto-provisions environment on first run
- Never overwrites existing database password
- Hardens insecure defaults
- Separate database (`app_staging`)

---

## 🔧 Workflow Configuration

### Branch Strategy

| Branch | Purpose | Auto-Deploy |
|--------|---------|-------------|
| `dispatch` | Current development | No |
| `develop` | Development branch | No |
| `master` | Stable code | → Staging |
| `main` | Production-ready | No (manual release) |

### Required Checks

Both deployment workflows wait for these checks:
- ✅ `CI` - All quality checks
- ✅ `test-docker-compose` - Docker integration test

### Self-Hosted Runners

Your deployment uses self-hosted runners:

**Production Runner:**
- Labels: Default self-hosted
- Runs on: Production server
- Access: `production.env` in `/home/github/.config/eugine-api/`

**Staging Runner:**
- Labels: `self-hosted`, `staging`
- Runs on: Staging server
- Access: `staging.env` in `/home/github/.config/eugine-api/`

---

## 🚀 How to Deploy

### Deploy to Staging

```bash
# 1. Commit changes
git add .
git commit -m "Your changes"

# 2. Push to master
git push origin master

# GitHub Actions will automatically:
# → Run CI checks
# → Deploy to staging.api.barrels.gd
```

### Deploy to Production

```bash
# 1. Merge to main (if not already)
git checkout main
git merge master

# 2. Create and push tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# 3. Create GitHub Release
# Go to: GitHub → Releases → Draft new release
# - Tag: v1.0.0
# - Title: v1.0.0
# - Description: Release notes
# - Publish release

# GitHub Actions will automatically:
# → Verify CI checks
# → Deploy to api.barrels.gd
# → Run health checks
```

---

## 🛠️ Environment Configuration

### CI Environment Variables

Set in workflows (no secrets needed):
```yaml
env:
  POSTGRES_SERVER: localhost
  POSTGRES_USER: app
  POSTGRES_PASSWORD: changethis
  SECRET_KEY: test-secret-key
```

### Server Environment Files

#### Production
**Location:** `/home/github/.config/eugine-api/production.env`

**Must contain:**
```env
ENVIRONMENT=production
DOMAIN=api.barrels.gd
STACK_NAME=barrels-api
PROJECT_NAME=barrels-api
POSTGRES_DB=app_prod
SECRET_KEY=<strong-secret>
POSTGRES_PASSWORD=<strong-password>
FIRST_SUPERUSER_PASSWORD=<strong-password>
```

#### Staging
**Location:** `/home/github/.config/eugine-api/staging.env`

**Auto-provisioned on first deploy** with:
- Staging domain: `staging.api.barrels.gd`
- Separate database: `app_staging`
- Strong auto-generated secrets

---

## 📝 Required GitHub Secrets

### None Required! 🎉

Your workflows use self-hosted runners which:
- ✅ Have direct access to server
- ✅ Use pre-configured environment files
- ✅ Don't need SSH keys in GitHub Secrets
- ✅ More secure (secrets stay on server)

### Optional Secrets (for notifications)

If you want deployment notifications:
- `SLACK_WEBHOOK_URL` - For Slack notifications
- `DISCORD_WEBHOOK` - For Discord notifications

---

## 🔍 Monitoring Workflows

### View Workflow Runs
1. Go to GitHub repository
2. Click **Actions** tab
3. View all workflows and their status

### Check Logs
1. Click on a workflow run
2. Click on a job
3. Expand steps to see logs

### Failed Deployment
Workflows automatically show extensive logs on failure:
- Prestart logs (migration issues)
- API logs (startup errors)
- DB logs (database issues)
- Proxy logs (routing issues)
- Sanitized environment (for debugging)

---

## 🎨 Code Quality Standards

All code must pass before merging:

### Formatting
```bash
# Auto-fix
./scripts/format.sh

# Or manually
uv run ruff format src scripts
```

### Linting
```bash
# Check
./scripts/lint.sh

# Or manually
uv run ruff check src scripts
```

### Type Checking
```bash
uv run mypy src
```

### Tests
```bash
# Full suite
./scripts/dev.sh test-cov

# Quick test
docker compose exec api python scripts/quick_test.py
```

---

## 🆘 Troubleshooting

### CI Workflow Fails

**Linting errors:**
```bash
# Fix locally
./scripts/format.sh
git add -A
git commit -m "Fix linting"
git push
```

**Tests fail:**
```bash
# Run tests locally
./scripts/dev.sh test-cov

# Fix issues, then push
```

### Deployment Fails

**Check self-hosted runner:**
```bash
# SSH to server
ssh user@your-server

# Check runner status
cd /path/to/actions-runner
./run.sh
```

**Check environment file:**
```bash
# On server
cat /home/github/.config/eugine-api/production.env | sed -E 's/(SECRET_KEY|PASSWORD)=.*/\1=****/'
```

**Manual deployment:**
```bash
# SSH to server
ssh user@your-server
cd ~/app

# Pull and deploy
docker compose -f docker-compose.yml -p barrels-api pull
docker compose -f docker-compose.yml -p barrels-api up -d
```

---

## 📊 Workflow Status Badges

Add to your README.md:

```markdown
![CI](https://github.com/yourusername/fast-back/workflows/CI/badge.svg)
![Test Docker Compose](https://github.com/yourusername/fast-back/workflows/Test%20Docker%20Compose/badge.svg)
```

---

## 🎓 Best Practices Implemented

### Security
- ✅ No secrets in workflow files
- ✅ Secrets stay on self-hosted servers
- ✅ Sanitized logs (passwords hidden)
- ✅ Vulnerability scanning with Trivy
- ✅ Guards against default passwords

### Reliability
- ✅ Waits for all CI checks before deploy
- ✅ Health checks after deployment
- ✅ Extensive error logging
- ✅ Automatic retry logic

### Performance
- ✅ BuildKit caching
- ✅ Concurrent workflow cancellation
- ✅ Parallel job execution
- ✅ Dependency caching with uv

### Maintainability
- ✅ Clear job names and steps
- ✅ Comprehensive comments
- ✅ Failure debugging built-in
- ✅ Consistent patterns across workflows

---

## 📚 Related Documentation

- **GITHUB_SECRETS.md** - Secrets configuration (if needed)
- **DEPLOYMENT.md** - Full deployment guide
- **DEPLOYMENT_SETUP.md** - Deployment setup instructions
- **env.production.example** - Production environment template
- **env.example** - Development environment template

---

## ✅ Verification

### Check Workflows are Active

```bash
# List all workflows
ls -la .github/workflows/

# Should see:
# - ci.yml
# - test-docker-compose.yml
# - deploy-production.yml
# - deploy-staging.yml
# - (and others)
```

### Test CI Locally

```bash
# Run same checks as CI
./scripts/format.sh
./scripts/lint.sh
./scripts/dev.sh test-cov
docker compose build -f Dockerfile.prod
```

### Simulate Deployment

```bash
# Build production image
docker build -f Dockerfile.prod -t test:latest .

# Run it
docker run -p 8000:8000 test:latest
```

---

## 🎯 Next Steps

1. ✅ Workflows aligned and fixed
2. ✅ Service names corrected (backend → api)
3. ✅ Branch triggers updated
4. ✅ Environment files created
5. ✅ Documentation complete

**Ready to deploy!** Push to master to test staging deployment. 🚀

---

**Last Updated**: October 14, 2025  
**Status**: ✅ Aligned & Production Ready

