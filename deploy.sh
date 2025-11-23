#!/bin/bash
# Simple deployment script for EC2
# Run this on your EC2 instance

set -e

echo "🚀 Starting deployment..."

# Pull latest changes if using git
if [ -d ".git" ]; then
    echo "📥 Pulling latest changes..."
    git pull
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 5

# Check service status
echo "✅ Service status:"
docker-compose ps

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "Access your services at:"
echo "  API:    http://$(curl -s ifconfig.me):8000"
echo "  UI:     http://$(curl -s ifconfig.me):8501"
echo "  Docs:   http://$(curl -s ifconfig.me):8000/docs"

