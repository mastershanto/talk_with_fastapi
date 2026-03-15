"""Seed script to populate database with sample data."""
import random
import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.models.user import User
from app.models.property import Property, PropertyType, PropertyStatus
from app.auth_utils import hash_password

# Database setup
engine = create_engine(str(settings.DATABASE_URL))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sample data generators
FIRST_NAMES = [
    "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry",
    "Iris", "Jack", "Karen", "Leo", "Mia", "Noah", "Olivia", "Peter",
    "Quinn", "Rachel", "Sam", "Tina", "Uma", "Victor", "Wendy", "Xavier",
    "Yara", "Zoe", "Aaron", "Bella", "Carlos", "Diana", "Ethan", "Fiona"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson", "Walker", "Young"
]

LOCATIONS = [
    "Downtown", "Uptown", "Westside", "Eastside", "North Hills", "South Bay",
    "Central Park", "Riverside", "Lakefront", "Mountain View", "Valley View",
    "Seaside", "Hillside", "Parkside", "Waterfront", "Midtown", "Suburbs",
    "Historic District", "Arts District", "Tech Park", "Garden District"
]

PROPERTY_TITLES = [
    "Beautiful Family Home", "Modern Apartment", "Spacious Villa",
    "Cozy Cottage", "Luxury Penthouse", "Urban Loft", "Country Estate",
    "Beach House", "Mountain Cabin", "Commercial Space", "Office Building",
    "Retail Store", "Warehouse", "Land Plot", "Investment Property",
    "Starter Home", "Dream House", "Historic Property", "New Construction",
    "Renovated Home", "Garden Property", "Waterfront Estate", "Hilltop Mansion"
]

DESCRIPTIONS = [
    "Perfect for families with great schools nearby",
    "Recently renovated with modern amenities",
    "Excellent investment opportunity",
    "Walking distance to shopping and dining",
    "Private and peaceful setting",
    "High rental yield potential",
    "Stunning views and spacious layout",
    "Move-in ready condition",
    "Great neighborhood with community activities",
    "Close to transportation and highways"
]


def _make_email(first: str, last: str) -> str:
    suffix = random.randint(1, 9999)
    return f"{first.lower()}.{last.lower()}{suffix}@example.com"


def generate_users(count: int) -> list[User]:
    """Generate sample users."""
    users = []
    for _ in range(count):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        name = f"{first_name} {last_name}"
        age = random.randint(18, 80)
        first, last = name.split(" ", 1)
        users.append(
            User(
                name=name,
                email=_make_email(first, last),
                password_hash=hash_password("password123"),
                role="user",
                agree_to_terms=True,
                is_premium=False,
                age=float(age),
            )
        )
    return users


def generate_properties(count: int, user_ids: list[int]) -> list[Property]:
    """Generate sample properties."""
    properties = []
    for _ in range(count):
        title = random.choice(PROPERTY_TITLES)
        description = random.choice(DESCRIPTIONS)
        price = round(random.uniform(50000, 2000000), 2)
        location = random.choice(LOCATIONS)
        property_type = random.choice(list(PropertyType))
        status = random.choice(list(PropertyStatus))
        area_sqft = round(random.uniform(800, 10000), 0)
        owner_id = random.choice(user_ids)

        properties.append(Property(
            title=title,
            description=description,
            price=price,
            location=location,
            property_type=property_type,
            status=status,
            area_sqft=area_sqft,
            owner_id=owner_id
        ))
    return properties


def seed_database(force: bool = False):
    """Populate database with sample data."""
    session = SessionLocal()

    try:
        # Check if data already exists
        user_count = session.query(User).count()
        if user_count > 0 and not force:
            print(f"⚠️  Database already contains {user_count} users. Use --force to re-seed.")
            return

        # Clear existing data if force is enabled
        if force and user_count > 0:
            print("🗑️  Clearing existing data...")
            session.query(Property).delete()
            session.query(User).delete()
            session.commit()
            print("✅ Existing data cleared")

        print("🌱 Starting database seeding...")

        # Generate and add users
        print("📝 Creating 100 users...")
        users = generate_users(100)
        session.add_all(users)
        session.commit()

        # Get user IDs
        user_ids = [user.id for user in session.query(User).all()]
        print(f"✅ Created {len(user_ids)} users")

        # Generate and add properties
        print("🏠 Creating 100+ properties...")
        properties = generate_properties(120, user_ids)  # 120 properties for variety
        session.add_all(properties)
        session.commit()

        property_count = session.query(Property).count()
        print(f"✅ Created {property_count} properties")

        print("🎉 Seeding completed successfully!")
        print(f"   - Users: {len(user_ids)}")
        print(f"   - Properties: {property_count}")

    except Exception as e:
        session.rollback()
        print(f"❌ Error during seeding: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed the database with sample data")
    parser.add_argument("--force", action="store_true", help="Force re-seeding (clears existing data)")
    args = parser.parse_args()

    seed_database(force=args.force)
