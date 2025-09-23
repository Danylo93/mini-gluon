#!/bin/bash

# Build script for Scaffold Forge
echo "🚀 Building Scaffold Forge..."

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: docker-compose.yml not found. Please run this script from the project root."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env file and add your GitHub token before running docker-compose up"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p ssl

# Build and start services
echo "🐳 Building and starting Docker containers..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are running
echo "🔍 Checking service status..."
docker-compose ps

# Show logs
echo "📋 Recent logs:"
docker-compose logs --tail=20

echo ""
echo "✅ Build complete!"
echo "🌐 Access the application at: http://localhost:8000"
echo "📊 API available at: http://localhost:8000/api"
echo ""
echo "📋 Useful commands:"
echo "  docker-compose logs -f          # Follow logs"
echo "  docker-compose down             # Stop services"
echo "  docker-compose restart          # Restart services"
echo ""
