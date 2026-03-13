# Real Estate Enterprise API - Educational Textbook Reference

> A production-ready FastAPI application designed as an educational textbook for learning enterprise Python web development.

## 📘 Learning Objectives

This project teaches you:

- **Enterprise Architecture** - How professional web applications are structured
- **FastAPI Patterns** - Dependency injection, routers, middleware
- **SQLAlchemy ORM** - Database modeling and relationships
- **Pydantic Validation** - Request/response schema design
- **CRUD Operations** - Reusable data access layer
- **Error Handling** - Custom exceptions and global handlers
- **Admin Interfaces** - SQLAdmin integration
- **Type Safety** - Full Python type hints
- **Best Practices** - Industry standards and conventions

## 🚀 Quick Start

```bash
# 1. Activate virtual environment
source .venv/bin/activate

# 2. Run the server
./run.sh

# 3. Visit API documentation
open http://localhost:8000/docs
```

## 📁 Project Structure

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed documentation of each module.

```
app/
├── config.py              # Configuration and settings
├── database.py            # SQLAlchemy setup
├── dependencies.py        # Dependency injection
├── exceptions.py          # Error handling
├── main.py                # Application factory
├── models/                # Database models
├── schemas/               # Validation schemas  
├── repositories/          # Repository pattern (data access)
└── routers/               # API endpoints
```

## 🎯 Naming Conventions

This project strictly follows Python naming conventions:

### Variables
```python
# Single instances: lowercase, snake_case
user = User(name="John")
property_listing = Property(title="House", price=500000)

# Collections: plural, snake_case
users_list = db.query(User).all()
properties_list = property_crud.get_multi(db)
```

### Functions & Methods
```python
# Descriptive verb + noun, lowercase
def get_user(user_id: int) -> User: ...
def create_property(payload: PropertyCreate) -> Property: ...
def list_properties(skip: int = 0, limit: int = 10) -> list[Property]: ...
```

### Classes
```python
# PascalCase, descriptive name
class PropertyResponse(BaseModel): ...
class CRUDBase(Generic): ...
class NotFoundException(AppException): ...
```

### Constants
```python
# UPPER_CASE for constants
MAX_PAGE_SIZE = 100
DEFAULT_PAGE_SIZE = 20
DATABASE_TIMEOUT = 30
```

## 📚 Learning Path

### Phase 1: Fundamentals (30 mins)
1. Read [ARCHITECTURE.md](./ARCHITECTURE.md)
2. Explore `app/models/property.py` - Understand ORM models
3. Explore `app/schemas/property.py` - Understand validation

### Phase 2: Intermediate (1 hour)
1. Study `app/crud/base.py` - Generic CRUD pattern
2. Study `app/crud/property.py` - Specific implementation
3. Study `app/routers/properties.py` - API endpoints

### Phase 3: Advanced (1.5 hours)
1. Study `app/dependencies.py` - Dependency injection
2. Study `app/exceptions.py` - Error handling
3. Study `app/main.py` - Application factory
4. Explore integration with SQLAdmin

### Phase 4: Hands-On (2+ hours)
1. Add a new field to Model
2. Update Schema to include new field
3. Test via API documentation
4. Create new endpoint following established patterns

## 🔌 API Endpoints

### Base URL
```
http://localhost:8000/api/v1
```

### Users Endpoints
```http
GET    /users              # List users (paginated)
GET    /users/{user_id}    # Get specific user
POST   /users              # Create user
PUT    /users/{user_id}    # Update user
DELETE /users/{user_id}    # Delete user
```

### Properties Endpoints
```http
GET    /properties              # List properties (paginated)
GET    /properties/{id}         # Get specific property
POST   /properties              # Create property
PUT    /properties/{id}         # Update property
DELETE /properties/{id}         # Delete property
```

## 📖 Documentation URLs

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Admin Panel**: http://localhost:8000/admin/
- **Architecture Guide**: [ARCHITECTURE.md](./ARCHITECTURE.md)

## 🏗️ Architecture Highlights

### 1. **Models** (app/models/)
SQLAlchemy ORM models define the database schema

### 2. **Schemas** (app/schemas/)
Pydantic models for request validation and response serialization

### 3. **CRUD Operations** (app/crud/)
Generic CRUD base class with specific implementations

### 4. **Routers** (app/routers/)
FastAPI endpoint definitions with dependency injection

### 5. **Dependency Injection** (app/dependencies.py)
Reusable services and database session management

## 🔄 Complete Data Flow

```
HTTP Request → Router → Dependencies → Validation → CRUD → Database → Response
```

## ✅ Best Practices Demonstrated

1. ✅ **Type Hints** - Full type safety
2. ✅ **Docstrings** - Comprehensive documentation
3. ✅ **Error Handling** - Custom exceptions
4. ✅ **Configuration** - Environment-based settings
5. ✅ **DRY Principle** - Generic base classes
6. ✅ **Separation of Concerns** - Clear module responsibilities
7. ✅ **Dependency Injection** - Loosely coupled services
8. ✅ **Database Sessions** - Proper lifecycle management
9. ✅ **Admin Interface** - SQLAdmin integration
10. ✅ **Pagination** - Validated, configurable

## 📝 Common Tasks

### Add a New Endpoint

1. Create route handler in `app/routers/`
2. Add request schema in `app/schemas/`
3. Add CRUD operation if needed
4. Test with Swagger UI

### Add a New Field

1. Update Model in `app/models/`
2. Update Schemas in `app/schemas/`
3. Database updates automatically
4. Test via API

## 🔧 Configuration

Edit `.env` to configure database and application settings.

## 📚 Learn More

- [ARCHITECTURE.md](./ARCHITECTURE.md) - Detailed architecture explanation
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org)
- [Pydantic Docs](https://docs.pydantic.dev)

---

**Happy Learning! 📚**
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
