#!/bin/bash

# Fast build script for Scaffold Forge
echo "🚀 Fast building Scaffold Forge..."

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: docker-compose.yml not found. Please run this script from the project root."
    exit 1
fi

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker não está rodando!"
    echo "💡 Execute: ./start-docker.sh"
    echo "   Ou inicie o Docker Desktop manualmente"
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

# Clean up previous builds
echo "🧹 Cleaning up previous builds..."
docker-compose down 2>/dev/null || true
docker system prune -f

# Build with optimized settings
echo "🐳 Building with ultra-optimized settings..."
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1
export BUILDKIT_PROGRESS=plain

# Build and start services
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 5

# Check if services are running
echo "🔍 Checking service status..."
docker-compose ps

# Show logs
echo "📋 Recent logs:"
docker-compose logs --tail=10

echo ""
echo "✅ Fast build complete!"
echo "🌐 Access the application at: http://localhost:8000"
echo "📊 API available at: http://localhost:8000/api"
echo ""
echo "📋 Useful commands:"
echo "  docker-compose logs -f          # Follow logs"
echo "  docker-compose down             # Stop services"
echo "  docker-compose restart          # Restart services"
echo ""
