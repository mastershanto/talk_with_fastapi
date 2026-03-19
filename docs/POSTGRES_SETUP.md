# PostgreSQL Setup Guide

This application is now configured to use PostgreSQL instead of SQLite. Follow these steps to set up PostgreSQL locally.

## macOS Setup (using Homebrew)

### 1. Install PostgreSQL

```bash
brew install postgresql@15
```

### 2. Start PostgreSQL Service

```bash
brew services start postgresql@15
```

### 3. Create Database and User

```bash
# Connect to PostgreSQL
psql postgres

# Inside psql, run these commands:
CREATE USER postgres WITH PASSWORD 'password';
ALTER USER postgres WITH SUPERUSER;
CREATE DATABASE real_estate_db OWNER postgres;

# Verify it worked
\l

# Exit psql
\q
```

### 4. Update Environment (if needed)

The `.env` file is already configured for local development:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/real_estate_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=real_estate_db
```

## Linux Setup (Ubuntu/Debian)

```bash
# Install PostgreSQL
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Start the service
sudo systemctl start postgresql

# Create database
sudo -u postgres createdb real_estate_db
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'password';"
```

## Windows Setup

1. Download PostgreSQL installer from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run the installer, set password to `password` for postgres user
3. During installation, ensure port is `5432`
4. Create database:
   ```sql
   CREATE DATABASE real_estate_db;
   ```

## Verify Your Setup

### Test Connection

```bash
# From your project directory
cd /Users/masterShanto/developments/talk_with_fastapi
source .venv/bin/activate

# Test the connection
python -c "
from app.database import engine
try:
    with engine.connect() as conn:
        result = conn.execute('SELECT 1')
        print('✅ PostgreSQL connection successful!')
except Exception as e:
    print(f'❌ Connection failed: {e}')
"
```

### Run the Application

```bash
# Activate virtual environment
source .venv/bin/activate

# Start the server
bash scripts/run.sh

# Or manually:
uvicorn app.main:app --reload
```

### Test an Endpoint

```bash
# Health check
curl http://localhost:8000/health | jq .

# List properties
curl http://localhost:8000/api/v1/properties/ | jq .

# Access admin panel
open http://localhost:8000/admin/
```

## Database Management

### View Database

```bash
psql real_estate_db
```

### Common psql Commands

```sql
-- List tables
\dt

-- Describe a table
\d properties

-- Show schemas
\dn

-- Exit
\q
```

### Backup Database

```bash
pg_dump real_estate_db > backup.sql
```

### Restore Database

```bash
psql real_estate_db < backup.sql
```

## Docker Alternative

If you prefer using Docker Postgres instead of local installation:

```bash
# Run PostgreSQL in Docker
docker run --name real_estate_db \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=real_estate_db \
  -p 5432:5432 \
  -d postgres:15

# Update .env:
DATABASE_URL=postgresql://postgres:password@localhost:5432/real_estate_db
```

## Troubleshooting

### Port Already in Use

If port 5432 is already in use:

```bash
# Find process using port 5432
lsof -i :5432

# Kill the process
kill -9 <PID>
```

### Connection Refused

- Ensure PostgreSQL service is running: `brew services list`
- Check credentials in `.env`
- Verify database exists: `psql postgres -l`

### Permission Denied

```bash
# Fix permissions
sudo chown $USER /usr/local/var/postgres
```

## Switching Back to SQLite (if needed)

Edit `.env`:

```env
DATABASE_URL=sqlite:///./dev.db
```

Then restart the application.

---

**Happy developing! 🚀**
