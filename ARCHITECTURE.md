<!-- # Real Estate Enterprise API - Educational Architecture Guide

Welcome! This project is a textbook-style implementation of an enterprise-grade FastAPI application. It follows industry best practices and is designed to teach you professional Python web development.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Core Concepts](#core-concepts)
3. [Data Flow](#data-flow)
├── domains/                  # 🧠 Domain modules (ports + use-cases)
│   ├── users/                # Users domain service + repository port
│   └── properties/           # Properties domain service + repository port
│
├── infrastructure/           # 🔩 Concrete adapters (DB, external services)
│   └── sqlalchemy/           # SQLAlchemy repository implementations
│
4. [File Descriptions](#file-descriptions)
5. [Learning Path](#learning-path)

## Project Structure

```
app/
├── config.py                # ⚙️  Configuration management (Settings)
├── database.py              # 🗄️  Database connection and session management
├── dependencies.py          # 🔌 Dependency injection (get_db, pagination)
├── exceptions.py            # ⚠️  Custom exceptions and error handlers
├── main.py                  # 🚀 Application factory and lifespan
├── __init__.py              # 📚 Package documentation
│
├── models/                  # 🏗️  SQLAlchemy ORM models (database schema)
│   ├── base.py             # BaseModel with common fields
│   ├── user.py             # User model
│   └── property.py         # Property/Land model
│
├── schemas/                 # ✅ Pydantic validation schemas
│   ├── common.py           # Shared schemas (MessageResponse, PaginatedResponse)
│   ├── user.py             # User schemas (UserCreate, UserUpdate, UserResponse)
│   └── property.py         # Property schemas (PropertyCreate, PropertyUpdate, PropertyResponse)
│
├── repositories/            # 🔄 Repository pattern (Create, Read, Update, Delete)
│   ├── base.py             # Generic CRUDBase class
│   ├── user.py             # User repository operations
│   └── property.py         # Property repository operations
│
└── routers/                 # 🛣️  API endpoint definitions
    ├── users.py            # User endpoints (/api/v1/users/*)
    └── properties.py       # Property endpoints (/api/v1/properties/*)
```

## Core Concepts

### 1. Models (app/models/)
**What:** Database schema definitions using SQLAlchemy ORM  
**Why:** Define database structure in Python for type safety and automatic migrations

```python
# Example: models/property.py
class Property(Base):
    __tablename__ = "properties"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    price: Mapped[float] = mapped_column(Float)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
```

### 2. Schemas (app/schemas/)
**What:** Pydantic models for request validation and response serialization  
**Why:** Validate input data, prevent over-posting, serialize database objects to JSON

```python
# Example: schemas/property.py
class PropertyCreate(BaseModel):
    """Schema for creating a property (POST request)"""
    title: str = Field(..., min_length=1, max_length=200)
    price: float = Field(..., gt=0)
    owner_id: int

class PropertyResponse(PropertyCreate):
    """Schema for API responses (includes database-generated fields)"""
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)  # Allows ORM conversion
```

### 3. Repository Pattern (app/repositories/)
**What:** Reusable database operations for all models using the Repository Pattern  
**Why:** DRY principle - define common operations once, use everywhere

```python
# Generic base class
class CRUDBase(Generic[ModelT, CreateSchemaT, UpdateSchemaT]):
    def get(self, db: Session, record_id: int) -> ModelT | None: ...
    def get_multi(self, db: Session, skip: int, limit: int) -> list[ModelT]: ...
    def create(self, db: Session, obj_in: CreateSchemaT) -> ModelT: ...
    def update(self, db: Session, db_obj: ModelT, obj_in: UpdateSchemaT) -> ModelT: ...
    def remove(self, db: Session, record_id: int) -> ModelT | None: ...

# Specific implementations
property_crud = CRUDProperty(Property)
user_crud = CRUDUser(User)
```

### 4. Routers (app/routers/)
**What:** FastAPI APIRouter instances that map HTTP requests to handlers  
**Why:** Organize endpoints by domain, keep handlers thin, and inject services

```python
# Example: routers/properties.py
@router.post("/", status_code=201)
def create_property(payload: PropertyCreate, service: PropertyServiceDep) -> dict:
    """Create a new property listing."""
    prop = service.create_property(payload)
    if not prop:
        raise NotFoundException(f"Owner (User {payload.owner_id}) not found.")
    return success_response(PropertyResponse.model_validate(prop), code=201)
```

### 5. Dependencies (app/dependencies.py)
**What:** Reusable dependency functions injected into routes  
**Why:** Keep routes clean, handle database sessions safely, validate pagination

```python
def get_db() -> Generator[Session, None, None]:
    """Dependency: provides database session and ensures cleanup"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Use in routes: db: DBSession (type alias with dependency)
```

### 6. Exception Handling (app/exceptions.py)
**What:** Custom exceptions converted to HTTP error responses  
**Why:** Consistent error format, proper HTTP status codes

```python
class NotFoundException(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Resource not found."

# Usage in routes:
raise NotFoundException("Property 42 not found.")
```

## Data Flow

### Typical Request Flow

```
HTTP Request (POST /api/v1/properties/)
    ↓
1. FastAPI Router receives request → properties.py
    ↓
2. Dependency Injection
   - get_db() provides database session
   - Pagination extracts skip/limit from query params
    ↓
3. Schema Validation
   - Pydantic validates JSON body → PropertyCreate
    ↓
4. Handler Function
    - PropertyService.create_property(payload)
    ↓
5. Use-case + Adapter
    - Service calls a repository port
    - Infrastructure adapter persists via SQLAlchemy CRUD
    ↓
6. Response Serialization
   - PropertyResponse.model_validate(db_property)
   - Converts SQLAlchemy model to JSON
    ↓
HTTP Response (201 Created + JSON body)
```

## File Descriptions

### Configuration Tier

**app/config.py** - Settings management via Pydantic
- Reads from environment variables and .env file
- Centralizes all configuration (database, API keys, etc.)
- Type-safe with validation

**app/database.py** - Database setup
- Creates SQLAlchemy engine (connection pool)
- Defines SessionLocal (session factory)
- Declares Base class for all models

### Dependency Injection

**app/dependencies.py** - Provides services to routes
- `get_db()`: Yields database sessions
- `PaginationParams`: Extracts and validates pagination
- `DBSession`: Type alias for dependency injection

### Error Handling

**app/exceptions.py** - Centralized exception handling
- Custom exception hierarchy
- Global exception handlers
- HTTP status code mapping

### Main Application

**app/main.py** - Application factory
- Creates FastAPI app instance
- Sets up middleware (CORS)
- Registers routers
- Defines lifespan (startup/shutdown)
- Configures SQLAdmin admin panel

### Data Models

**app/models/** - SQLAlchemy ORM models
- `base.py`: TimestampMixin for created_at/updated_at
- `user.py`: User model with relationships
- `property.py`: Property model with owner reference

### Request/Response Schemas

**app/schemas/** - Pydantic validation models
- `common.py`: MessageResponse, PaginatedResponse
- `user.py`: User schemas
- `property.py`: Property schemas

### Database Operations

**app/repositories/** - Repository pattern implementations
- `base.py`: Generic CRUDBase class
- `user.py`: User CRUD with custom queries
- `property.py`: Property repository operations

### API Endpoints

**app/routers/** - HTTP endpoint definitions
- `users.py`: User CRUD endpoints
- `properties.py`: Property CRUD endpoints

## Learning Path

### Beginner Level
1. Start with `app/config.py` - understand configuration
2. Read `app/models/user.py` - learn SQLAlchemy basics
3. Read `app/schemas/user.py` - understand Pydantic validation
4. Read `app/routers/users.py` - see how endpoints use models/schemas

### Intermediate Level
1. Study `app/repositories/base.py` - understand generics and DRY principles
2. Read `app/dependencies.py` - learn dependency injection
3. Study `app/exceptions.py` - understand error handling
4. Read `app/routers/properties.py` - see real-world endpoint implementation

### Advanced Level
1. Study `app/main.py` - understand application factory pattern
2. Learn about SQLAdmin integration for admin panel
3. Study the relationship between models and schemas
4. Understand the complete data flow

## API Endpoints

### Users
- `GET /api/v1/users/` - List users with pagination
- `GET /api/v1/users/{user_id}` - Get single user
- `POST /api/v1/users/` - Create user
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

### Properties
- `GET /api/v1/properties/` - List properties with pagination
- `GET /api/v1/properties/{property_id}` - Get single property
- `POST /api/v1/properties/` - Create property
- `PUT /api/v1/properties/{property_id}` - Update property
- `DELETE /api/v1/properties/{property_id}` - Delete property

## Admin Panel

Access SQLAdmin at: http://localhost:8000/admin/
- Manage Users and Properties directly from the web UI
- No need for raw SQL queries
- Real-time data updates

## Key Design Patterns

### 1. Repository Pattern (app/repositories/)
Abstraction layer between business logic and database

### 2. Factory Pattern (app/main.py)
Create application instances with configuration

### 3. Dependency Injection (app/dependencies.py)
Provide services without tight coupling

### 4. Schema Separation
Create/Update/Response schemas for flexibility

### 5. Middleware Architecture
CORS, error handling at application level

## Naming Conventions

### Variables
- `user`, `property` - single instances
- `users`, `properties` - collections
- `db` - database session
- `crud_obj` - CRUD operations instance

### Functions
- `get_all_users()` → `list_users()`
- `fetch_user()` → `get_user()`
- `add_property()` → `create_property()`

### Classes
- `UserModel` → `User` (models are clear from folder)
- `UserSchema` → `UserResponse` (purpose-specific naming)
- `UserCRUD` → `CRUDUser` (consistent with patterns)

### Endpoints
- `/api/v1/resources/` - List and create
- `/api/v1/resources/{id}` - Get, update, delete
- Follow REST conventions

## Best Practices Demonstrated

✅ **Type Safety** - Full type hints throughout  
✅ **DRY Principle** - Generic CRUD base class  
✅ **Separation of Concerns** - Models, schemas, CRUD, routers  
✅ **Dependency Injection** - Services provided, not created in routes  
✅ **Error Handling** - Custom exceptions, consistent error format  
✅ **Documentation** - Docstrings, type hints as documentation  
✅ **Configuration Management** - Environment-based settings  
✅ **Database Sessions** - Proper session lifecycle management  

---

**Ready to dive deeper?** Start with the `/ARCHITECTURE.md` files in each module or explore the source code! -->
