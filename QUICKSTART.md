<!-- # Quick Start Commands

## 🚀 Run Server (3 ways)

### 1. Using the run script (Easiest):
```bash
./run.sh
```

### 2. Direct uvicorn command:
```bash
source .venv/bin/activate
uvicorn app.app:app --reload
```

### 3. With custom host/port:
```bash
source .venv/bin/activate
uvicorn app.app:app --reload --host 0.0.0.0 --port 8000
```

## 🛑 Stop Server
```bash
# Press Ctrl+C in terminal
# OR
pkill -f uvicorn
```

## 📝 Common Commands

### Database commands:
```bash
# Connect to PostgreSQL
psql users_db

# View users
psql users_db -c "SELECT * FROM users;"

# Drop and recreate database
dropdb users_db && createdb users_db
```

### API Testing:
```bash
# Get all users
curl http://localhost:8000/users

# Get single user
curl http://localhost:8000/users/1

# Create user
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "age": 25}'

# Update user
curl -X PUT http://localhost:8000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Name"}'

# Delete user
curl -X DELETE http://localhost:8000/users/1
```

## 📚 Access API Documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔧 Troubleshooting

### If port 8000 is busy:
```bash
# Kill any process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn app.app:app --reload --port 8001
```

### If database connection fails:
```bash
# Check PostgreSQL is running
brew services list | grep postgresql

# Start PostgreSQL
brew services start postgresql@14

# Check database exists
psql -l | grep users_db
``` -->
