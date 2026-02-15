"""
Main FastAPI application
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import Base, engine, get_db
from app.routers import users, items
from app import models


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup"""
    try:
        # Try to create tables with a timeout
        from sqlalchemy.exc import OperationalError, ProgrammingError
        import signal
        import types
        
        def timeout_handler(signum: int, frame: types.FrameType | None) -> None:
            raise TimeoutError("Database initialization timed out")
        
        # Set a 15-second timeout for database initialization
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(15)
        
        try:
            Base.metadata.create_all(bind=engine)
            signal.alarm(0)  # Cancel alarm
            print("✓ Database tables created")
            
            # Try to add sample data
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
        except TimeoutError:
            signal.alarm(0)  # Cancel alarm
            print("⚠ Database initialization timed out (Aiven server not responding)")
            print("  → Tables will be created on first request")
        except (OperationalError, ProgrammingError) as e:
            signal.alarm(0)  # Cancel alarm
            print(f"⚠ Database error: {str(e)[:100]}")
            print("  → Continuing without database initialization")
            
    except Exception as e:
        print(f"⚠ Unexpected error during startup: {type(e).__name__}: {str(e)[:100]}")
        print("  → App will continue running")
    
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
app.include_router(items.router)


@app.get("/", tags=["root"])
def read_root():
    return {"message": "Aiven PostgreSQL এর সাথে আপনার FastAPI কানেক্টেড!"}


@app.get("/test-db")
def test_db(db: Session = Depends(get_db)) -> dict[str, str]:
    # ডাটাবেস থেকে একটি সিম্পল কোয়েরি চালানো
    result = db.execute(text("SELECT version();")).scalar_one_or_none()
    return {"postgresql_version": result or "unknown"}
