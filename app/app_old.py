import os
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


# ============= Configuration =============
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://masterShanto@localhost:5432/users_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# ============= Models =============
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)


class UserResponse(BaseModel):
    id: int
    name: str
    age: int

    model_config = ConfigDict(from_attributes=True)


# ============= Dependencies =============
def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============= Lifespan Events =============
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup"""
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            sample_users = [
                User(name="Alice", age=25),
                User(name="Bob", age=30),
                User(name="Charlie", age=35),
            ]
            db.add_all(sample_users)
            db.commit()
    finally:
        db.close()
    
    yield


# ============= Application =============
app = FastAPI(
    title="User Management API",
    description="Simple REST API for managing users with PostgreSQL",
    version="1.0.0",
    lifespan=lifespan
)


# ============= Routes =============
@app.get("/", tags=["Root"])
def root():
    """Root endpoint"""
    return {"message": "Welcome to User Management API"}


@app.get("/users", response_model=List[UserResponse], tags=["Users"])
def get_all_users(db: Session = Depends(get_db)):
    """Get all users"""
    users = db.query(User).all()
    return users


@app.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return user