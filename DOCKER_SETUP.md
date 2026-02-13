<!-- # FastAPI Docker Setup Guide

## ✅ Current Status

### API Server
- **Status**: Running ✓
- **URL**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Database
- **Current Mode**: SQLite (local file)
- **File Location**: `/Users/masterShanto/developments/talk_with_fastapi/users.db`
- **Status**: Read-only issue with write operations

---

## 🐳 Docker Setup Files Created

### 1. **docker-compose.yml**
- PostgreSQL 15 Alpine service (port 5432)
- FastAPI application service (port 8000)
- Automatic database initialization
- Health checks for database readiness
- Persistent volume for database

### 2. **docker-start.sh**
Quick start script with:
- Docker availability check
- Container startup management
- PostgreSQL readiness wait
- API readiness verification
- Log viewing instructions

### 3. **Updated Configuration Files**
- `.env` - Environment variables for PostgreSQL
- `database.py` - PostgreSQL support with fallback
- `Dockerfile` - Data directory creation for SQLite

---

## 🚀 Quick Start with Docker

### Option 1: Ensure Docker is Running
```bash
# Check Docker status
docker ps

# If Docker daemon not running, start it
open -a Docker  # macOS
```

### Option 2: Run the Quick Start Script
```bash
cd /Users/masterShanto/developments/talk_with_fastapi
chmod +x docker-start.sh
./docker-start.sh
```

### Option 3: Manual Docker Compose
```bash
cd /Users/masterShanto/developments/talk_with_fastapi

# Stop any existing containers
docker-compose down -v

# Start fresh
docker-compose up -d

# View logs
docker-compose logs -f api
```

---

## 📝 Docker Compose Configuration

### Services
1. **PostgreSQL Database (`db`)**
   - Image: `postgres:15-alpine`
   - Port: 5432
   - Username: `avnadmin`
   - Password: See `.env` file (not committed to git for security)
   - Database: `defaultdb`
   - Health Check: Active
   - Persistent Volume: `postgres_data`

2. **FastAPI Application (`api`)**
   - Builds from `docker/Dockerfile`
   - Port: 8000
   - Environment: PostgreSQL via Docker network (`db:5432`)
   - Hot Reload: Enabled (mounts source code)
   - Depends on: PostgreSQL health check

---

## 🔧 Environment Configuration

**In Docker** (automatically set from .env):
```bash
DATABASE_URL=postgresql://avnadmin:YOUR_PASSWORD@db:5432/defaultdb
```

**Locally** (from .env file):
```bash
DATABASE_URL=postgresql://avnadmin:YOUR_PASSWORD@localhost:5432/defaultdb
```

> ⚠️ **Security:** Never commit actual passwords to version control. Use `.env` file (not tracked by git) or GitHub Secrets for CI/CD.

---

## 📊 Testing the Setup

### Test API Endpoints
```bash
# Get all users
curl http://localhost:8000/users/

# Create a new user
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","age":30}'

# Get user by ID
curl http://localhost:8000/users/1

# Update user
curl -X PUT http://localhost:8000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Doe","age":31}'

# Delete user
curl -X DELETE http://localhost:8000/users/1
```

### Check Database
```bash
# Connect to PostgreSQL in Docker
docker-compose exec db psql -U avnadmin -d defaultdb

# List tables
\dt

# View users
SELECT * FROM users;

# Exit
\q
```

---

## 🛑 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 5432
lsof -ti:5432 | xargs kill -9
```

### Docker Daemon Not Running
```bash
# macOS
open -a Docker

# Wait for Docker to start
sleep 10
```

### Container Startup Issues
```bash
# View logs
docker-compose logs -f

# Rebuild image
docker-compose build --no-cache

# Remove old containers
docker-compose down -v
docker system prune
```

### Database Connection Issues
```bash
# Test database connection
docker-compose exec api python -c "from app.database import DATABASE_URL; print(DATABASE_URL)"

# Check if database tables exist
docker-compose exec db psql -U avnadmin -d defaultdb -c "SELECT * FROM users;"
```

---

## 📦 What Happens on Startup

1. PostgreSQL container starts and initializes the database
2. Health check waits up to 50 seconds for PostgreSQL to be ready
3. FastAPI application builds (on first run)
4. API container starts and waits for database
5. Database tables are auto-created on first connection
6. Sample data is inserted if database is empty

---

## 💾 Persistent Data

- PostgreSQL data is stored in Docker volume: `talk_with_fastapi_postgres_data`
- Data persists even when containers are stopped
- To reset: `docker-compose down -v` (removes volume)

---

## 🔄 Development Workflow

### Running with Auto-Reload
Code changes are automatically detected (source mounted as volume)
```bash
docker-compose logs -f api
```

### Rebuilding After Dependency Changes
```bash
docker-compose build --no-cache api
docker-compose up -d
```

### Database Schema Changes
If you modify models.py, the tables will be auto-created on next startup

---

## 📚 Additional Resources

- Docker Compose Docs: https://docs.docker.com/compose/
- PostgreSQL Docker: https://hub.docker.com/_/postgres  
- FastAPI Documentation: https://fastapi.tiangolo.com/
- SQLAlchemy ORM: https://docs.sqlalchemy.org/

---

## ✨ Next Steps

1. **Restart Docker**: `open -a Docker` (if not running)
2. **Run Setup Script**: `./docker-start.sh`
3. **Access API**: Open http://localhost:8000/docs
4. **Test Endpoints**: Use the Swagger UI or curl commands
5. **View Logs**: `docker-compose logs -f`
6. **Stop Containers**: `docker-compose down`
 -->
