"""
Seed admin user with email and password for testing.
Run this script to create initial test user: python seed_admin.py
"""
import sys
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.models.user import User
from app.auth_utils import hash_password

# Database setup
engine = create_engine(str(settings.DATABASE_URL))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables if they don't exist
from app.database import Base
Base.metadata.create_all(bind=engine)

def seed_admin_user():
    """Create an admin user for testing."""
    db = SessionLocal()
    
    try:
        # Check if admin user already exists
        existing_user = db.query(User).filter(User.email == "admin@gmail.com").first()
        if existing_user:
            print("✓ Admin user already exists")
            return
        
        # Create admin user
        admin_user = User(
            name="Admin User",
            email="admin@gmail.com",
            password_hash=hash_password("password123"),
            email_verified_at=datetime.utcnow(),
            role="admin",
            avatar=None,
            agree_to_terms=True,
            is_premium=False,
            age=23.0,
            gender="male",
            height=181.0,
            weight=62.0,
            goal="Gain muscle mass",
            days_in_week=None,
            time_in_day=None,
            workout_duration=None,
            refer_photo=None,
            target_bmi=None,
            target_body_fat=None,
            target_weight=None,
        )
        
        db.add(admin_user)
        db.commit()
        
        print("✓ Admin user created successfully!")
        print(f"  Email: admin@gmail.com")
        print(f"  Password: password123")
        print(f"  Role: admin")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error creating admin user: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    print("🌱 Seeding admin user...")
    seed_admin_user()
    print("✅ Done!")
