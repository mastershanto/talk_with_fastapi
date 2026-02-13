"""
CRUD operations for database
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app import models, schemas


def get_user(db: Session, user_id: int) -> models.User | None:
    """Get a single user by ID"""
    try:
        return db.query(models.User).filter(models.User.id == user_id).first()
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        raise


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
    """Get list of users with pagination"""
    try:
        return db.query(models.User).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return []


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user"""
    try:
        db_user = models.User(name=user.name, age=user.age)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error: {e}")
        raise


def update_user(
    db: Session, 
    user_id: int, 
    user_update: schemas.UserUpdate
) -> models.User | None:
    """Update an existing user"""
    try:
        db_user = get_user(db, user_id)
        if not db_user:
            return None
        
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error: {e}")
        raise


def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user"""
    try:
        db_user = get_user(db, user_id)
        if not db_user:
            return False
        
        db.delete(db_user)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error: {e}")
        raise
