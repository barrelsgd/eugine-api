#!/bin/bash
# Setup script for FastAPI development environment

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

echo -e "${GREEN}FastAPI Development Environment Setup${NC}"
echo -e "${GREEN}======================================${NC}"
echo ""

# Check if Docker is running
echo -e "${CYAN}Checking Docker...${NC}"
if ! docker version > /dev/null 2>&1; then
    echo -e "${RED}Error: Docker is not running. Please start Docker.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker is running${NC}"

# Check Docker Compose version
echo -e "${CYAN}Checking Docker Compose...${NC}"
if ! docker compose version > /dev/null 2>&1; then
    echo -e "${RED}Error: Docker Compose is not available.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose is available${NC}"

# Check if .env exists
echo -e "${CYAN}Checking environment configuration...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env from .env.example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
    echo ""
    echo -e "${YELLOW}IMPORTANT: Edit .env and set secure values for:${NC}"
    echo -e "${YELLOW}  - SECRET_KEY (generate with: openssl rand -base64 32)${NC}"
    echo -e "${YELLOW}  - FIRST_SUPERUSER${NC}"
    echo -e "${YELLOW}  - FIRST_SUPERUSER_PASSWORD${NC}"
    echo -e "${YELLOW}  - POSTGRES_PASSWORD${NC}"
    echo ""
else
    echo -e "${GREEN}✓ .env file exists${NC}"
fi

# Create traefik-public network if it doesn't exist
echo -e "${CYAN}Setting up Docker networks...${NC}"
if ! docker network ls --format "{{.Name}}" | grep -q "^traefik-public$"; then
    echo -e "${YELLOW}Creating traefik-public network...${NC}"
    docker network create traefik-public
    echo -e "${GREEN}✓ traefik-public network created${NC}"
else
    echo -e "${GREEN}✓ traefik-public network exists${NC}"
fi

echo ""
echo -e "${GREEN}Setup complete!${NC}"
echo ""
echo -e "${CYAN}Next steps:${NC}"
echo -e "${WHITE}1. Review and edit .env file with secure values${NC}"
echo -e "${WHITE}2. Start development environment:${NC}"
echo -e "${YELLOW}   ./scripts/dev.sh start${NC}"
echo -e "${WHITE}   OR${NC}"
echo -e "${YELLOW}   docker compose watch${NC}"
echo ""
echo -e "${CYAN}Services will be available at:${NC}"
echo -e "${WHITE}  - API: http://localhost:8000${NC}"
echo -e "${WHITE}  - API Docs: http://localhost:8000/docs${NC}"
echo -e "${WHITE}  - Adminer: http://localhost:8081${NC}"
echo -e "${WHITE}  - MailCatcher: http://localhost:1080${NC}"
echo -e "${WHITE}  - Traefik: http://localhost:8090${NC}"
echo ""
