# User Management API

A modern, scalable FastAPI application with PostgreSQL database.

## 📁 Project Structure

```
talk_with_fastapi/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── app.py               # Main application entry point
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py              # CRUD operations
│   ├── dependencies.py      # Dependency injection
│   └── routers/
│       ├── __init__.py
│       └── users.py         # User routes
├── requirements.txt
└── README.md
```

## 🎯 File Descriptions

### `app.py`
Main application file with:
- FastAPI app initialization
- Lifespan events
- Router inclusion

### `database.py`
Database configuration:
- SQLAlchemy engine
- Session factory
- Base class for models

### `models.py`
SQLAlchemy ORM models:
- Database table definitions
- Relationships

### `schemas.py`
Pydantic models for:
- Request validation
- Response serialization
- Data validation

### `crud.py`
Database operations:
- Create, Read, Update, Delete functions
- Reusable database logic

### `dependencies.py`
Dependency injection:
- Database session management
- Authentication (future)

### `routers/users.py`
User API endpoints:
- GET, POST, PUT, DELETE operations
- Route definitions

## 🚀 Running the Application

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the server
uvicorn app.app:app --reload
```

## 📚 API Endpoints

### Users
- `GET /users` - Get all users (with pagination)
- `GET /users/{user_id}` - Get user by ID
- `POST /users` - Create new user
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

## 📖 API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔧 Environment Variables

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/users_db
```

## 🌟 Features

- ✅ Clean architecture
- ✅ Separation of concerns
- ✅ Type hints throughout
- ✅ CRUD operations
- ✅ Error handling
- ✅ Input validation
- ✅ Pagination support
- ✅ Auto-generated API docs

## 🔮 Future Enhancements

- [ ] Authentication & Authorization
- [ ] Tests (pytest)
- [ ] Logging
- [ ] Migrations (Alembic)
- [ ] Docker support
- [ ] CI/CD pipeline
