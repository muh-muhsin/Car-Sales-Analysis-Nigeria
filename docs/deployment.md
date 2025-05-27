# Cars360 Deployment Guide

## Overview

This guide covers deploying Cars360 to production environments including smart contracts, backend API, and frontend application.

## Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.9+
- PostgreSQL 13+
- Redis 6+
- Docker (optional)
- Clarinet CLI
- Hiro Wallet

## Environment Setup

### 1. Clone Repository
```bash
git clone https://github.com/muhsinmuhammad/Cars360.git
cd Cars360
```

### 2. Environment Configuration
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Install Dependencies
```bash
# Frontend
cd frontend && npm install

# Backend
cd ../backend && pip install -r requirements.txt

# Smart Contracts
cd ../blockchain && clarinet install
```

## Smart Contract Deployment

### 1. Testnet Deployment

```bash
cd blockchain

# Configure Clarinet.toml for testnet
clarinet deploy --testnet

# Verify deployment
clarinet console
```

### 2. Mainnet Deployment

```bash
# Update network configuration
export STACKS_NETWORK=mainnet

# Deploy to mainnet (requires STX for fees)
clarinet deploy --mainnet

# Update contract addresses in environment
```

### 3. Contract Verification

```bash
# Test contract functions
clarinet console

# Register test dataset
(contract-call? .dataset-registry register-dataset 
  u"ipfs://QmTest123" 
  u1000000 
  u"{\"title\":\"Test Dataset\"}")

# Check dataset
(contract-call? .dataset-registry get-dataset u1)
```

## Backend Deployment

### 1. Database Setup

```bash
# Create PostgreSQL database
createdb cars360

# Run migrations
cd backend
alembic upgrade head
```

### 2. Redis Setup

```bash
# Start Redis server
redis-server

# Verify connection
redis-cli ping
```

### 3. Local Development

```bash
cd backend

# Start development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Production Deployment

#### Using Docker

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build and run
docker build -t cars360-backend .
docker run -p 8000:8000 cars360-backend
```

#### Using systemd

```ini
# /etc/systemd/system/cars360-backend.service
[Unit]
Description=Cars360 Backend API
After=network.target

[Service]
Type=simple
User=cars360
WorkingDirectory=/opt/cars360/backend
Environment=PATH=/opt/cars360/venv/bin
ExecStart=/opt/cars360/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable cars360-backend
sudo systemctl start cars360-backend
```

## Frontend Deployment

### 1. Build Application

```bash
cd frontend

# Install dependencies
npm install

# Build for production
npm run build
```

### 2. Static Deployment (Vercel)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

### 3. Self-hosted Deployment

```bash
# Start production server
npm start

# Or use PM2
npm install -g pm2
pm2 start npm --name "cars360-frontend" -- start
```

### 4. Nginx Configuration

```nginx
# /etc/nginx/sites-available/cars360
server {
    listen 80;
    server_name cars360.ng www.cars360.ng;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## IPFS Setup

### 1. Local IPFS Node

```bash
# Install IPFS
wget https://dist.ipfs.io/go-ipfs/v0.17.0/go-ipfs_v0.17.0_linux-amd64.tar.gz
tar -xvzf go-ipfs_v0.17.0_linux-amd64.tar.gz
sudo mv go-ipfs/ipfs /usr/local/bin/

# Initialize and start
ipfs init
ipfs daemon
```

### 2. Pinata (Managed IPFS)

```bash
# Configure Pinata API keys
export PINATA_API_KEY=your-api-key
export PINATA_SECRET_KEY=your-secret-key
```

## SSL/TLS Configuration

### 1. Let's Encrypt with Certbot

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d cars360.ng -d www.cars360.ng

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Monitoring and Logging

### 1. Application Monitoring

```bash
# Install monitoring tools
npm install -g pm2
pip install sentry-sdk

# Configure PM2 monitoring
pm2 install pm2-server-monit
```

### 2. Log Management

```bash
# Configure log rotation
sudo nano /etc/logrotate.d/cars360

# Content:
/var/log/cars360/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 cars360 cars360
}
```

## Database Backup

### 1. Automated Backups

```bash
#!/bin/bash
# backup-db.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups/cars360"
DB_NAME="cars360"

mkdir -p $BACKUP_DIR

pg_dump $DB_NAME | gzip > $BACKUP_DIR/cars360_$DATE.sql.gz

# Keep only last 30 days
find $BACKUP_DIR -name "cars360_*.sql.gz" -mtime +30 -delete
```

```bash
# Add to crontab
0 2 * * * /opt/scripts/backup-db.sh
```

## Security Checklist

- [ ] Environment variables secured
- [ ] Database credentials rotated
- [ ] SSL/TLS certificates configured
- [ ] Firewall rules configured
- [ ] Rate limiting enabled
- [ ] CORS properly configured
- [ ] API keys secured
- [ ] Regular security updates
- [ ] Backup strategy implemented
- [ ] Monitoring alerts configured

## Performance Optimization

### 1. Database Optimization

```sql
-- Create indexes for common queries
CREATE INDEX idx_datasets_owner ON datasets(owner);
CREATE INDEX idx_datasets_created_at ON datasets(created_at);
CREATE INDEX idx_datasets_price ON datasets(price);
```

### 2. Caching Strategy

```python
# Redis caching for API responses
import redis
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_result(expiration=300):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            cached = redis_client.get(cache_key)
            
            if cached:
                return json.loads(cached)
            
            result = func(*args, **kwargs)
            redis_client.setex(cache_key, expiration, json.dumps(result))
            return result
        return wrapper
    return decorator
```

### 3. CDN Configuration

```bash
# Configure CloudFlare or AWS CloudFront
# Cache static assets and API responses
# Enable compression and minification
```

## Troubleshooting

### Common Issues

1. **Contract deployment fails**
   - Check STX balance for fees
   - Verify network configuration
   - Check Clarinet.toml syntax

2. **Database connection errors**
   - Verify PostgreSQL is running
   - Check connection string
   - Ensure database exists

3. **IPFS upload failures**
   - Check IPFS daemon status
   - Verify API endpoint
   - Check file size limits

4. **Frontend build errors**
   - Clear node_modules and reinstall
   - Check environment variables
   - Verify TypeScript configuration

### Log Locations

- **Frontend:** `~/.pm2/logs/`
- **Backend:** `/var/log/cars360/`
- **Nginx:** `/var/log/nginx/`
- **PostgreSQL:** `/var/log/postgresql/`

## Support

For deployment assistance:
- Documentation: [docs.cars360.ng](https://docs.cars360.ng)
- GitHub Issues: [Cars360 Repository](https://github.com/muhsinmuhammad/Cars360)
- Email: devops@cars360.ng
- Discord: [Cars360 Community](https://discord.gg/cars360)
