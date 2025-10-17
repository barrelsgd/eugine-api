# GitHub Secrets Configuration

Complete guide for setting up GitHub Secrets for CI/CD workflows.

---

## 📋 Required Secrets

### For CI/CD Workflows

#### 1. SSH Deployment Secrets

**For deploying via SSH to your server:**

| Secret Name | Description | How to Get |
|------------|-------------|------------|
| `SSH_PRIVATE_KEY` | Private SSH key for server access | Generate with `ssh-keygen` |
| `SSH_HOST` | Server IP or hostname | Your server IP (e.g., `123.45.67.89`) |
| `SSH_USER` | SSH username | Usually `root` or your username |

**Setup:**
```bash
# Generate SSH key pair (if not exists)
ssh-keygen -t ed25519 -C "github-actions@yourapp.com"

# Copy public key to server
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@your-server

# Add private key to GitHub Secrets
cat ~/.ssh/id_ed25519
# Copy the output and add to GitHub Secrets as SSH_PRIVATE_KEY
```

#### 2. Docker Registry Secrets

**For GitHub Container Registry (automatic):**
- `GITHUB_TOKEN` is automatically provided by GitHub Actions
- No manual configuration needed

**For Docker Hub (alternative):**

| Secret Name | Description |
|------------|-------------|
| `DOCKERHUB_USERNAME` | Your Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token |

#### 3. Application Secrets

**Required for deployment:**

| Secret Name | Description | Example |
|------------|-------------|---------|
| `PRODUCTION_API_URL` | Production API URL | `https://api.yourdomain.com` |
| `STACK_NAME` | Docker stack name | `fast-back` |

**Optional (for notifications):**

| Secret Name | Description | How to Get |
|------------|-------------|------------|
| `SLACK_WEBHOOK_URL` | Slack webhook for notifications | Create in Slack: Incoming Webhooks |
| `DISCORD_WEBHOOK` | Discord webhook for notifications | Server Settings → Integrations → Webhooks |

---

## 🔐 How to Add Secrets to GitHub

### Via GitHub UI

1. Go to your repository on GitHub
2. Click **Settings** (repository settings)
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Enter the secret name and value
6. Click **Add secret**

### Required Secrets for Basic Setup

Minimal configuration for CD workflow:

```
SSH_PRIVATE_KEY=<your-ssh-private-key>
SSH_HOST=<your-server-ip>
SSH_USER=<your-ssh-username>
PRODUCTION_API_URL=https://api.yourdomain.com
```

---

## 🎯 Secrets by Deployment Method

### Option 1: Docker Swarm

```
SSH_PRIVATE_KEY=<key>
SSH_HOST=<host>
SSH_USER=<user>
STACK_NAME=fast-back
```

### Option 2: Kubernetes

```
KUBE_CONFIG=<base64-encoded-kubeconfig>
```

**Get kubeconfig:**
```bash
cat ~/.kube/config | base64
```

### Option 3: AWS ECS

```
AWS_ACCESS_KEY_ID=<key>
AWS_SECRET_ACCESS_KEY=<secret>
AWS_REGION=us-east-1
```

### Option 4: Azure Container Apps

```
AZURE_CREDENTIALS=<service-principal-json>
```

**Create service principal:**
```bash
az ad sp create-for-rbac \
  --name "github-actions" \
  --role contributor \
  --scopes /subscriptions/<subscription-id>/resourceGroups/<resource-group> \
  --sdk-auth
```

### Option 5: DigitalOcean

```
DIGITALOCEAN_ACCESS_TOKEN=<your-token>
```

---

## 📝 Environment Variables vs Secrets

### Use GitHub Secrets For:
✅ Passwords and API keys  
✅ SSH keys  
✅ Database credentials  
✅ OAuth tokens  
✅ Any sensitive data

### Use Environment Variables For:
✅ Public configuration  
✅ Feature flags  
✅ Non-sensitive URLs  
✅ Build settings

---

## 🔧 Setting Up Production Secrets

### Step 1: Generate Secure Values

```bash
# Generate SECRET_KEY
openssl rand -base64 32

# Generate passwords
openssl rand -base64 32

# Generate JWT secret
openssl rand -hex 32
```

### Step 2: Add to Server

Create `.env` file on your server:

```bash
ssh user@your-server
cd ~/app
nano .env
```

Add content from `env.production.example`:

```env
ENVIRONMENT=production
SECRET_KEY=<generated-secret>
POSTGRES_PASSWORD=<generated-password>
FIRST_SUPERUSER_PASSWORD=<generated-password>
# ... etc
```

### Step 3: Add to GitHub Secrets

Only add secrets needed by GitHub Actions:
- SSH credentials
- Notification webhooks
- Deployment tokens

**Don't duplicate all .env variables in GitHub Secrets!**

---

## 🛡️ Security Best Practices

### 1. Rotate Secrets Regularly
- Change passwords every 90 days
- Rotate API keys quarterly
- Update SSH keys annually

### 2. Use Different Secrets for Each Environment
- Development
- Staging
- Production

### 3. Never Log Secrets
```yaml
# ❌ BAD
- name: Debug
  run: echo ${{ secrets.SECRET_KEY }}

# ✅ GOOD
- name: Deploy
  env:
    SECRET_KEY: ${{ secrets.SECRET_KEY }}
  run: ./deploy.sh
```

### 4. Use Least Privilege
- Give secrets only the permissions they need
- Use read-only tokens where possible
- Limit scope of access tokens

### 5. Monitor Secret Usage
- Check GitHub Actions logs regularly
- Set up alerts for failed deployments
- Audit secret access

---

## 🚀 Quick Setup Guide

### Minimal Setup (SSH Deployment)

1. **Generate SSH key:**
```bash
ssh-keygen -t ed25519 -f ~/.ssh/github_actions
```

2. **Add public key to server:**
```bash
ssh-copy-id -i ~/.ssh/github_actions.pub user@your-server
```

3. **Add secrets to GitHub:**

```bash
# SSH_PRIVATE_KEY
cat ~/.ssh/github_actions

# Copy output and add to GitHub Secrets
```

4. **Test deployment:**
```bash
# Push to main branch
git push origin main

# Check GitHub Actions tab
```

---

## 📊 Secrets Checklist

### Before First Deployment

- [ ] `SSH_PRIVATE_KEY` - Added and tested
- [ ] `SSH_HOST` - Correct server IP/hostname
- [ ] `SSH_USER` - Correct username
- [ ] `PRODUCTION_API_URL` - Set to production domain
- [ ] Server `.env` file created with production values
- [ ] SSH key added to server's `~/.ssh/authorized_keys`
- [ ] Server has Docker and Docker Compose installed
- [ ] Traefik network created (`docker network create traefik-public`)
- [ ] GitHub Actions enabled in repository

### Optional Enhancements

- [ ] `SLACK_WEBHOOK_URL` - For deployment notifications
- [ ] `DISCORD_WEBHOOK` - For deployment notifications
- [ ] `SENTRY_DSN` - For error tracking
- [ ] Multiple environment secrets (staging, production)
- [ ] Backup secrets configuration

---

## 🆘 Troubleshooting

### Secret Not Found
```
Error: Secret SSH_PRIVATE_KEY not found
```

**Solution:**
1. Check secret name matches exactly (case-sensitive)
2. Verify secret is added to repository (not organization)
3. Check branch has access to secrets

### SSH Connection Failed
```
Permission denied (publickey)
```

**Solution:**
1. Verify private key format is correct (include header/footer)
2. Check public key is in server's `authorized_keys`
3. Test SSH manually: `ssh -i <key-file> user@server`

### Deployment Failed
```
Error: Cannot connect to server
```

**Solution:**
1. Check `SSH_HOST` is correct
2. Verify server is running
3. Check firewall allows SSH (port 22)
4. Verify `SSH_USER` has permissions

---

## 📚 Additional Resources

- [GitHub Encrypted Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [SSH Key Management](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [Docker Secrets](https://docs.docker.com/engine/swarm/secrets/)
- [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)

---

**Last Updated**: October 14, 2025  
**Status**: ✅ Ready for Production

