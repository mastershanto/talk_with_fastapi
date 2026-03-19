# Quick Start Commands

## 🚀 Run Server (3 ways)

### 1. Using the run script (Easiest):
```bash
bash scripts/run.sh
```

### 2. Direct uvicorn command:
```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

### 3. With custom host/port:
```bash
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
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
psql real_estate_db

# View users
psql real_estate_db -c "SELECT * FROM users;"

# Drop and recreate database
dropdb real_estate_db && createdb real_estate_db
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
  -d '{"name": "Updated User", "age": 26}'

# Delete user
curl -X DELETE http://localhost:8000/users/1
```

### Development tools:
```bash
# Format code
make format

# Run linter
make lint

# Run tests
make test

# Run full CI (lint + typecheck + test)
make ci

# Type check
make typecheck

# Architecture guard
make arch-guard

# Database migration
make db-upgrade

# Create migration
make db-revision
```

### View API docs:
```bash
# Swagger UI
open http://localhost:8000/docs

# ReDoc
open http://localhost:8000/redoc

# Admin panel
open http://localhost:8000/admin/
```

## 🧰 Project Setup (One Time)

```bash
# 1. Clone and navigate
cd talk_with_fastapi

# 2. Create virtual environment
python3 -m venv .venv

# 3. Activate virtual environment
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements-dev.txt

# 5. Install pre-commit hooks
pre-commit install

# 6. Setup PostgreSQL
bash scripts/setup_postgres.sh

# 7. Run migrations
python scripts/migrate_db.py

# 8. Seed test data
python scripts/seed_admin.py

# 9. Start the server
bash scripts/run.sh
```

## 📚 More Commands

See `Makefile` for all available commands:
```bash
make help
```

See individual documentation files:
- [docs/README.md](./README.md) - Overview
- [docs/ARCHITECTURE.md](./ARCHITECTURE.md) - Architecture explanation
- [docs/AUTHENTICATION_SETUP.md](./AUTHENTICATION_SETUP.md) - Auth system
- [docs/POSTGRES_SETUP.md](./POSTGRES_SETUP.md) - PostgreSQL setup
