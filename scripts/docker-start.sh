#!/bin/bash

# Start FastAPI App with Local PostgreSQL via Docker Compose
# This script handles all the setup and running of the application and database

set -e

echo "========================================"
echo "🚀 Talk with FastAPI - Docker Setup"
echo "========================================"
echo ""

# Check if Docker is running
if ! docker ps > /dev/null 2>&1; then
    echo "❌ Docker daemon is not running"
    echo "Please start Docker Desktop or run: open -a Docker"
    exit 1
fi

echo "✓ Docker is running"
echo ""

# Navigate to project root
cd "$(dirname "$0")"

echo "📦 Building and starting containers..."
echo ""

# Build and start containers
docker-compose down -v 2>/dev/null || true
sleep 2
docker-compose up -d

# Wait for PostgreSQL to be ready
echo ""
echo "⏳ Waiting for PostgreSQL to be ready..."
for i in {1..30}; do
    if docker-compose exec -T db pg_isready -U avnadmin > /dev/null 2>&1; then
        echo "✓ PostgreSQL is ready"
        break
    fi
    echo -n "."
    sleep 1
done

echo ""
echo "⏳ Waiting for API to start..."
sleep 5

# Check if API is responding
for i in {1..10}; do
    if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
        echo "✓ API is ready"
        break
    fi
    echo -n "."
    sleep 1
done

echo ""
echo "========================================"
echo "✅ Everything is running!"
echo "========================================"
echo ""
echo "📚 API Documentation:"
echo "   Swagger UI: http://localhost:8000/docs"
echo "   ReDoc:      http://localhost:8000/redoc"
echo ""
echo "🗄️  Database:"
echo "   Host:     localhost"
echo "   Port:     5432"
echo "   User:     avnadmin"
echo "   Database: defaultdb"
echo ""
echo "💾 To view logs:"
echo "   docker-compose logs -f api    # API logs"
echo "   docker-compose logs -f db     # Database logs"
echo ""
echo "🛑 To stop the containers:"
echo "   docker-compose down"
echo ""
