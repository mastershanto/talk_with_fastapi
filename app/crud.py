"""
CRUD operations for database
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from app import models, schemas
from app.database import Base, engine


def ensure_tables_exist():
    """Create tables if they don't exist"""
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"⚠ Could not create tables: {str(e)[:50]}")


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
    except (OperationalError, SQLAlchemyError) as e:
        print(f"Database error: {e}")
        # Try to create tables and retry
        ensure_tables_exist()
        return []


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user"""
    try:
        # Ensure tables exist before writing
        ensure_tables_exist()
        
        db_user = models.User(name=user.name, age=user.age)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except (OperationalError, SQLAlchemyError) as e:
        db.rollback()
        print(f"Database error during create: {e}")
        raise


def update_user(
    db: Session, 
    user_id: int, 
    user_update: schemas.UserUpdate
) -> models.User | None:
    """Update an existing user"""
    try:
        ensure_tables_exist()
        
        db_user = get_user(db, user_id)
        if not db_user:
            return None
        
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
        return db_user
    except (OperationalError, SQLAlchemyError) as e:
        db.rollback()
        print(f"Database error during update: {e}")
        raise


def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user"""
    try:
        ensure_tables_exist()
        
        db_user = get_user(db, user_id)
        if not db_user:
            return False
        
        db.delete(db_user)
        db.commit()
        return True
    except (OperationalError, SQLAlchemyError) as e:
        db.rollback()
        print(f"Database error during delete: {e}")
        raise


# ---- Item CRUD operations ----
def get_item(db: Session, item_id: int) -> models.Item | None:
    """Get a single item by ID"""
    try:
        return db.query(models.Item).filter(models.Item.id == item_id).first()
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        raise


def get_items(db: Session, skip: int = 0, limit: int = 100) -> list[models.Item]:
    """Get list of items with pagination"""
    try:
        return db.query(models.Item).offset(skip).limit(limit).all()
    except (OperationalError, SQLAlchemyError) as e:
        print(f"Database error: {e}")
        ensure_tables_exist()
        return []


def create_item(db: Session, item: schemas.ItemCreate) -> models.Item:
    """Create a new item"""
    try:
        ensure_tables_exist()
        db_item = models.Item(
            title=item.title,
            description=item.description,
            price=item.price,
            is_active=item.is_active,
            owner_id=item.owner_id,
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except (OperationalError, SQLAlchemyError) as e:
        db.rollback()
        print(f"Database error during create_item: {e}")
        raise


def delete_item(db: Session, item_id: int) -> bool:
    """Delete an item"""
    try:
        ensure_tables_exist()
        db_item = get_item(db, item_id)
        if not db_item:
            return False
        db.delete(db_item)
        db.commit()
        return True
    except (OperationalError, SQLAlchemyError) as e:
        db.rollback()
        print(f"Database error during delete_item: {e}")
        raise
