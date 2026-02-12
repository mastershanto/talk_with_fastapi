"""
SQLAlchemy database models
"""
from sqlalchemy import Column, Integer, String
from app.database import Base


class User(Base):
    """User database model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, age={self.age})>"
