# 🐳 AspireHR Docker Deployment Guide

This guide helps you deploy AspireHR on various free cloud platforms using Docker.

## 🚀 Quick Local Testing

### Prerequisites
- Docker installed on your system
- Git installed

### Steps:
```bash
# 1. Clone the repository
git clone https://github.com/innopay-suresh/commi.git
cd commi

# 2. Build and run with Docker Compose
docker-compose up --build

# 3. Access your app
# Open browser: http://localhost:8000
# Username: Administrator
# Password: admin
```

## ☁️ Free Cloud Deployment Options

### Option 1: Railway (Recommended - $5 free credit)

1. **Sign up** at https://railway.app
2. **Connect GitHub** repository
3. **Deploy** from GitHub:
   - Repository: `innopay-suresh/commi`
   - Branch: `main`
   - Build Command: `docker build -t aspirehr .`
   - Start Command: `docker run -p $PORT:8000 aspirehr`

### Option 2: Render (Free tier available)

1. **Sign up** at https://render.com
2. **New Web Service** → Import from GitHub
3. **Configuration**:
   - Repository: `https://github.com/innopay-suresh/commi`
   - Branch: `main`
   - Runtime: `Docker`
   - Start Command: `./start.sh`

### Option 3: Fly.io (Free tier available)

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login and deploy
flyctl auth login
flyctl launch --name aspirehr-app
flyctl deploy
```

### Option 4: Google Cloud Run (Free tier: 2M requests/month)

```bash
# Build and push to Google Container Registry
docker build -t gcr.io/YOUR-PROJECT/aspirehr .
docker push gcr.io/YOUR-PROJECT/aspirehr

# Deploy to Cloud Run
gcloud run deploy aspirehr \
  --image gcr.io/YOUR-PROJECT/aspirehr \
  --platform managed \
  --port 8000 \
  --allow-unauthenticated
```

### Option 5: AWS ECS (Free tier: 1 year)

1. **Push to Amazon ECR**:
```bash
# Build and tag
docker build -t aspirehr .
docker tag aspirehr:latest YOUR-ACCOUNT.dkr.ecr.region.amazonaws.com/aspirehr:latest

# Push to ECR
aws ecr get-login-password --region region | docker login --username AWS --password-stdin YOUR-ACCOUNT.dkr.ecr.region.amazonaws.com
docker push YOUR-ACCOUNT.dkr.ecr.region.amazonaws.com/aspirehr:latest
```

2. **Create ECS Task Definition** and **Service**

## 🔧 Environment Variables

For production deployment, set these environment variables:

```bash
FRAPPE_SITE_NAME=your-domain.com
ADMIN_PASSWORD=your-secure-password
REDIS_URL=redis://localhost:6379
```

## 📝 Custom Domain Setup

Most platforms allow custom domains:
- Railway: Settings → Custom Domain
- Render: Settings → Custom Domain
- Fly.io: `flyctl certs create your-domain.com`
- Cloud Run: Cloud Console → Domain mapping

## 🛠️ Troubleshooting

### Common Issues:

1. **Port binding**: Ensure your platform uses the correct port (8000)
2. **Memory limits**: Increase memory allocation if needed
3. **Build timeout**: Some platforms have build time limits
4. **Environment variables**: Set required variables in platform settings

### Support:
- Check platform-specific documentation
- Use platform support channels
- Check GitHub issues for common problems

## 💰 Cost Comparison

| Platform | Free Tier | Monthly Cost |
|----------|-----------|--------------|
| Railway | $5 credit | $5+ |
| Render | 750 hours | $7+ |
| Fly.io | 3 shared CPUs | $0-10 |
| Google Cloud Run | 2M requests | $0-20 |
| AWS ECS | 1 year free | $10+ |

## 🎯 Recommended Approach

For beginners: **Railway** - Easiest setup, good free tier
For developers: **Fly.io** - Great performance, flexible
For enterprises: **Google Cloud Run** - Scalable, reliable
