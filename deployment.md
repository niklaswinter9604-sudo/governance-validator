@"
# Deployment Guide

## Local Development (POC)
conda activate validator
python app/app.py

text

## Staging / Production Deployment

### Option 1: Docker (Recommended)
docker build -t governance-validator:1.0.0 -f docker/Dockerfile .
docker run -p 8080:8080 governance-validator:1.0.0

text

### Option 2: Cloud (AWS)
- EC2 Instance (t3.small)
- Docker Container
- Auto-scaling Group
- Application Load Balancer

### Option 3: Kubernetes
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

text

## Monitoring
- Prometheus metrics on /metrics
- Grafana dashboard
- CloudWatch logs

## Resource Requirements
- **Minimum:** 256MB RAM, 1 CPU
- **Recommended:** 500MB RAM, 2 CPU
- **Peak Load:** 2GB RAM, 4 CPU

## Cost Estimate
- AWS t3.small: ~€50/month
- Data storage: ~€10/month
- Total: ~€60/month
"@ | Out-File DEPLOYMENT.md -Encoding UTF8
