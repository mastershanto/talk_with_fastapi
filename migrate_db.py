"""
Database migration tool to sync schema with our models
This will drop and recreate all tables - use with caution!
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from app.database import Base
from app import models

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ DATABASE_URL not found in environment")
    exit(1)

print(f"🔧 Connecting to database...")
engine = create_engine(DATABASE_URL)

# Drop all tables
print("⚠️  Dropping all existing tables...")
with engine.begin() as conn:
    # Get all table names
    result = conn.execute(text("""
        SELECT tablename FROM pg_tables 
        WHERE schemaname = 'public'
    """))
    tables = [row[0] for row in result]
    
    if tables:
        print(f"   Found tables: {', '.join(tables)}")
        for table in tables:
            print(f"   Dropping table: {table}")
            conn.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))
    else:
        print("   No tables found")

# Create all tables from models
print("✨ Creating tables from models...")
Base.metadata.create_all(bind=engine)

# Verify tables were created
with engine.begin() as conn:
    result = conn.execute(text("""
        SELECT tablename FROM pg_tables 
        WHERE schemaname = 'public'
    """))
    tables = [row[0] for row in result]
    print(f"✓ Created tables: {', '.join(tables)}")

print("✅ Database schema migration complete!")
