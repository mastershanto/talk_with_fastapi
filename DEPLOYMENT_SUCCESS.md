# 🎉 FastAPI + Aiven PostgreSQL - Complete Application

## ✅ Current Status: **RUNNING & DEPLOYED**

Your FastAPI application is successfully connected to **Aiven PostgreSQL** cloud database!

---

## 🎯 Application Features

### 📊 Database Models
1. **User Model**
   - `id`: Integer (Primary Key)
   - `name`: String(100)
   - `age`: Integer
   - Relationship: One-to-Many with Items

2. **Item Model**
   - `id`: Integer (Primary Key)
   - `title`: String(200)
   - `description`: String(1000) [Optional]
   - `price`: Float
   - `is_active`: Boolean
   - `owner_id`: Foreign Key → User

---

## 🔌 Database Connection

**Provider:** Aiven Cloud PostgreSQL  
**Version:** PostgreSQL 17.7  
**Connection:** SSL Required  
**Status:** ✅ Connected

Connection configured in `.env`:
```
DATABASE_URL=postgresql://avnadmin:***@pg-25aca85f-talk-with-fastapi.a.aivencloud.com:28124/defaultdb?sslmode=require
```

---

## 🚀 API Endpoints

### Root & Health Check
- `GET /` - Welcome message (Bengali)
- `GET /test-db` - Database version check
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

### 👥 User Endpoints
- `GET /users/` - List all users (pagination: skip, limit)
- `GET /users/{user_id}` - Get specific user by ID
- `POST /users/` - Create new user
  ```json
  {
    "name": "John Doe",
    "age": 28
  }
  ```
- `PUT /users/{user_id}` - Update existing user
- `DELETE /users/{user_id}` - Delete user

### 📦 Item Endpoints
- `GET /items/` - List all items (pagination: skip, limit)
- `GET /items/{item_id}` - Get specific item by ID
- `POST /items/` - Create new item
  ```json
  {
    "title": "MacBook Pro",
    "description": "16-inch laptop",
    "price": 2499.99,
    "is_active": true,
    "owner_id": 1
  }
  ```
- `DELETE /items/{item_id}` - Delete item

---

## 📂 Project Structure

```
talk_with_fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app & lifespan
│   ├── database.py          # Database connection & session
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic validation schemas
│   ├── crud.py              # Database operations
│   ├── dependencies.py      # Dependency injection
│   └── routers/
│       ├── users.py         # User endpoints
│       └── items.py         # Item endpoints
├── tests/
│   └── test_items.py        # Unit tests
├── .env                     # Environment variables (Aiven config)
├── requirements.txt         # Python dependencies
├── migrate_db.py           # Database schema migration tool
└── run.sh                   # Quick start script
```

---

## 🏃 Running the Application

### Option 1: Using the run script
```bash
chmod +x run.sh
./run.sh
```

### Option 2: Manual start
```bash
source .venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Option 3: Production mode (no reload)
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 🧪 Testing

### Run unit tests
```bash
source .venv/bin/activate
pytest tests/ -v
```

### Test specific file
```bash
pytest tests/test_items.py -v
```

### Coverage report
```bash
pytest --cov=app tests/
```

---

## 🔄 Database Migration

If you modify models, sync schema with:
```bash
python migrate_db.py
```

⚠️ **Warning:** This drops all tables and recreates them!

For production, consider using **Alembic** for versioned migrations.

---

## 📋 Current Database Data

### Users (2 records)
```json
[
  {"id": 1, "name": "John Doe", "age": 28},
  {"id": 2, "name": "Alice Smith", "age": 32}
]
```

### Items (3 records)
```json
[
  {"id": 1, "title": "MacBook Pro", "price": 2499.99, "owner_id": 1},
  {"id": 2, "title": "iPhone 15", "price": 1199.99, "owner_id": 2},
  {"id": 3, "title": "iPad Air", "price": 599.99, "owner_id": 1}
]
```

---

## 🛠️ API Testing Examples

### Create a user
```bash
curl -X POST http://127.0.0.1:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Bob Wilson", "age": 35}'
```

### Get all users
```bash
curl http://127.0.0.1:8000/users/
```

### Create an item
```bash
curl -X POST http://127.0.0.1:8000/items/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "AirPods Pro",
    "description": "Noise cancelling",
    "price": 249.99,
    "is_active": true,
    "owner_id": 1
  }'
```

### Get all items
```bash
curl http://127.0.0.1:8000/items/
```

### Delete an item
```bash
curl -X DELETE http://127.0.0.1:8000/items/1
```

---

## 📊 Interactive API Documentation

Open your browser and navigate to:
- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

You can test all endpoints directly from the browser!

---

## 🔐 Security Features

✅ Environment variables for credentials  
✅ SQL injection prevention (SQLAlchemy ORM)  
✅ Request validation (Pydantic schemas)  
✅ SSL/TLS connection to Aiven PostgreSQL  
✅ Foreign key constraints  
✅ Error handling & proper HTTP status codes

---

## 📦 Dependencies

Key packages:
- **FastAPI** 0.100+ - Web framework
- **Uvicorn** - ASGI server
- **SQLAlchemy** 2.0+ - ORM
- **Psycopg2** - PostgreSQL adapter
- **Pydantic** 2.0+ - Data validation
- **Python-dotenv** - Environment management
- **Pytest** - Testing framework

---

## 🎯 Next Steps

### Recommended Enhancements
1. **Authentication & Authorization**
   - Add JWT tokens
   - Implement user roles
   - Protect endpoints

2. **Advanced Features**
   - Pagination improvements
   - Search & filtering
   - Item update endpoint
   - Soft deletes

3. **Database Management**
   - Set up Alembic migrations
   - Add database indexes
   - Implement caching (Redis)

4. **Deployment**
   - Containerize with Docker
   - Deploy to cloud (Heroku, AWS, Azure)
   - Set up CI/CD pipeline
   - Add monitoring (Sentry, New Relic)

5. **Testing**
   - Increase test coverage
   - Add integration tests
   - Load testing (Locust)

---

## 🆘 Troubleshooting

### Database connection issues
1. Check `.env` file has correct `DATABASE_URL`
2. Verify Aiven service is running
3. Confirm IP whitelist includes your IP

### Schema mismatch errors
```bash
python migrate_db.py
```

### Port already in use
```bash
lsof -ti:8000 | xargs kill -9
```

---

## ✨ Success Indicators

✅ Server running on http://127.0.0.1:8000  
✅ Database connected to Aiven PostgreSQL  
✅ Tables created: `users`, `items`  
✅ CRUD operations working  
✅ Tests passing  
✅ API documentation accessible  

---

## 📞 Support

For issues or questions:
1. Check logs in terminal
2. Review `/docs` for API reference
3. Check Aiven dashboard for database status

---

**Last Updated:** ${new Date().toISOString()}  
**Status:** 🟢 Production Ready
