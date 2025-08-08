# Aarogya Unified Platform - Deployment Guide

## Overview
This guide covers multiple deployment options for the Aarogya health platform, including cloud platforms, VPS servers, and containerized deployments.

## Table of Contents
1. [Local Production Setup](#local-production-setup)
2. [Heroku Deployment](#heroku-deployment)
3. [Vercel + Railway Deployment](#vercel--railway-deployment)
4. [AWS Deployment](#aws-deployment)
5. [Docker Deployment](#docker-deployment)
6. [VPS Deployment](#vps-deployment)

---

## 1. Local Production Setup

### Prerequisites
```bash
# Ensure you have:
- Node.js 16+
- Python 3.9+
- Git
```

### Steps
```bash
# 1. Build frontend for production
cd frontend
npm run build

# 2. Install production dependencies
cd ../backend
pip install -r requirements.txt

# 3. Set environment variables
export FLASK_ENV=production
export SECRET_KEY=your-super-secure-secret-key

# 4. Start with production server
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

---

## 2. Heroku Deployment

### Frontend (React) on Heroku

#### Step 1: Prepare Frontend
```bash
cd frontend
# Add build script to package.json if not present
npm install -g create-react-app
```

#### Step 2: Create Heroku App
```bash
# Install Heroku CLI first
npm install -g heroku

# Login to Heroku
heroku login

# Create app for frontend
heroku create aarogya-frontend

# Set buildpack
heroku buildpacks:set heroku/nodejs -a aarogya-frontend

# Deploy
git subtree push --prefix frontend heroku main
```

### Backend (Flask) on Heroku

#### Step 1: Create Procfile
```bash
cd backend
echo "web: gunicorn app:app" > Procfile
```

#### Step 2: Update requirements.txt
```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

#### Step 3: Deploy Backend
```bash
# Create app for backend
heroku create aarogya-backend

# Set Python buildpack
heroku buildpacks:set heroku/python -a aarogya-backend

# Set environment variables
heroku config:set FLASK_ENV=production -a aarogya-backend
heroku config:set SECRET_KEY=your-secret-key -a aarogya-backend

# Deploy
git subtree push --prefix backend heroku main
```

---

## 3. Vercel + Railway Deployment

### Frontend on Vercel

#### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

#### Step 2: Deploy Frontend
```bash
cd frontend
vercel --prod
# Follow prompts to connect GitHub repo
```

#### Step 3: Vercel Configuration
Create `frontend/vercel.json`:
```json
{
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

### Backend on Railway

#### Step 1: Create Railway Account
Visit [Railway.app](https://railway.app) and create account

#### Step 2: Deploy Backend
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
cd backend
railway init

# Deploy
railway up
```

---

## 4. AWS Deployment

### Frontend on AWS S3 + CloudFront

#### Step 1: Build and Upload
```bash
cd frontend
npm run build

# Install AWS CLI
pip install awscli

# Configure AWS credentials
aws configure

# Create S3 bucket
aws s3 mb s3://aarogya-frontend

# Upload build files
aws s3 sync dist/ s3://aarogya-frontend --delete

# Enable website hosting
aws s3 website s3://aarogya-frontend --index-document index.html
```

#### Step 2: CloudFront Distribution
```bash
# Create CloudFront distribution (via AWS Console)
# Point to S3 bucket origin
# Enable compression
# Set default root object to index.html
```

### Backend on AWS EC2 + RDS

#### Step 1: Launch EC2 Instance
```bash
# Choose Amazon Linux 2 AMI
# t3.micro for testing, t3.small+ for production
# Configure security groups (ports 22, 80, 443, 5001)
```

#### Step 2: Setup EC2
```bash
# SSH into instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Install dependencies
sudo yum update -y
sudo yum install python3 python3-pip git nginx -y

# Clone repository
git clone https://github.com/your-repo/aarogya.git
cd aarogya/backend

# Install Python dependencies
pip3 install -r requirements.txt
pip3 install gunicorn

# Create systemd service
sudo nano /etc/systemd/system/aarogya.service
```

#### Step 3: Systemd Service Configuration
```ini
[Unit]
Description=Aarogya Flask App
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/aarogya/backend
Environment=PATH=/home/ec2-user/.local/bin
ExecStart=/home/ec2-user/.local/bin/gunicorn -w 4 -b 127.0.0.1:5001 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Step 4: Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 5. Docker Deployment

### Create Docker Files

#### Frontend Dockerfile
```dockerfile
# frontend/Dockerfile
FROM node:18-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### Backend Dockerfile
```dockerfile
# backend/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "4", "app:app"]
```

#### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "5001:5001"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=your-secret-key
    volumes:
      - ./backend:/app

  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: aarogya
      POSTGRES_USER: aarogya_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### Deploy with Docker
```bash
# Build and run
docker-compose up --build -d

# View logs
docker-compose logs -f

# Scale services
docker-compose up --scale backend=3
```

---

## 6. VPS Deployment (DigitalOcean/Linode)

### Step 1: Server Setup
```bash
# Create droplet with Ubuntu 22.04
# SSH into server
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install dependencies
apt install -y python3 python3-pip nodejs npm nginx git certbot python3-certbot-nginx
```

### Step 2: Deploy Application
```bash
# Clone repository
git clone https://github.com/your-repo/aarogya.git
cd aarogya

# Setup backend
cd backend
pip3 install -r requirements.txt
pip3 install gunicorn

# Setup frontend
cd ../frontend
npm install
npm run build

# Copy build to nginx directory
cp -r dist/* /var/www/html/
```

### Step 3: Configure Nginx
```nginx
# /etc/nginx/sites-available/aarogya
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /var/www/html;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:5001/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Step 4: SSL Certificate
```bash
# Enable site
ln -s /etc/nginx/sites-available/aarogya /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx

# Get SSL certificate
certbot --nginx -d your-domain.com
```

---

## Environment Variables

### Production Environment Variables

#### Frontend (.env.production)
```env
VITE_API_BASE_URL=https://api.your-domain.com
VITE_APP_NAME=Aarogya Health Platform
VITE_APP_VERSION=1.0.0
```

#### Backend (.env)
```env
FLASK_ENV=production
SECRET_KEY=your-super-secure-secret-key-here
DATABASE_URL=postgresql://user:password@localhost/aarogya
CORS_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

---

## Database Migration (Production)

### PostgreSQL Setup
```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE aarogya;
CREATE USER aarogya_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE aarogya TO aarogya_user;
\q
```

### Flask-Migrate (Optional)
```bash
pip install Flask-Migrate
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

## Monitoring and Maintenance

### Process Monitoring
```bash
# Install PM2 for Node.js apps
npm install -g pm2

# Use systemd for Python apps
sudo systemctl enable aarogya
sudo systemctl start aarogya
```

### Log Management
```bash
# Setup log rotation
sudo nano /etc/logrotate.d/aarogya

# Monitor logs
tail -f /var/log/nginx/access.log
journalctl -u aarogya -f
```

### Backup Strategy
```bash
# Database backup
pg_dump aarogya > backup_$(date +%Y%m%d).sql

# Application backup
tar -czf app_backup_$(date +%Y%m%d).tar.gz /path/to/aarogya
```

---

## Cost Estimates (Monthly)

### Small Scale (Testing)
- **Heroku**: $14/month (2 dynos)
- **Vercel + Railway**: $5-10/month
- **AWS t3.micro**: $8-12/month
- **DigitalOcean**: $5-10/month

### Medium Scale (Production)
- **AWS**: $50-100/month
- **DigitalOcean**: $20-40/month
- **Google Cloud**: $30-60/month

### Large Scale (Enterprise)
- **AWS**: $200+/month
- **Custom VPS**: $100+/month
- **Managed services**: $300+/month

---

## Quick Deploy Commands

### Heroku Quick Deploy
```bash
# One command deploy to Heroku
./deploy-heroku.sh
```

### Docker Quick Deploy
```bash
# One command Docker deploy
docker-compose up -d --build
```

### VPS Quick Deploy
```bash
# One command VPS deploy
./deploy-vps.sh your-server-ip
```

Choose the deployment method that best fits your needs, budget, and technical requirements!
