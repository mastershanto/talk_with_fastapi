"""
Main FastAPI application
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import Base, engine
from app.routers import users
from app import models


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup"""
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        # Add sample data if empty
        from app.database import SessionLocal
        db = SessionLocal()
        try:
            if db.query(models.User).count() == 0:
                sample_users = [
                    models.User(name="Alice", age=25),
                    models.User(name="Bob", age=30),
                    models.User(name="Charlie", age=35),
                    models.User(name="Shawon", age=35),
                    models.User(name="Sabber", age=37),
                ]
                db.add_all(sample_users)
                db.commit()
                print("✓ Sample data added")
        finally:
            db.close()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"⚠ Database initialization failed: {e}")
        print("⚠ App will continue running without database")
    
    yield


# Create FastAPI app
app = FastAPI(
    title="User Management API",
    description="A simple REST API for managing users with PostgreSQL",
    version="1.0.0",
    lifespan=lifespan
)


# Include routers
app.include_router(users.router)


@app.get("/", tags=["root"])
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to User Management API",
        "docs": "/docs",
        "version": "1.0.0"
    }
