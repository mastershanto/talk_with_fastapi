"""
Database configuration and session management
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env file
load_dotenv()

# Database URL from environment or default to PostgreSQL in Docker
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://avnadmin:changeme@db:5432/defaultdb"  # Docker PostgreSQL - set actual password in .env
)

# PostgreSQL (use after whitelisting IP in Aiven):
# Set DATABASE_URL in .env file with actual credentials

# Configure engine based on database type
if DATABASE_URL.startswith("sqlite"):
    # SQLite configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False
    )
    print("✓ Using SQLite database (local file)")
else:
    # PostgreSQL configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            "connect_timeout": 10,
            "options": "-c statement_timeout=30000"
        },
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        echo=False
    )
    print("✓ Using PostgreSQL database")

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# SQLALCHEMY_DATABASE_URL alias (compatibility with some examples)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# ডাটাবেস সেশন পাওয়ার ফাংশন
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
