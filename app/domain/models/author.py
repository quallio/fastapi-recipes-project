"""
SQLAlchemy model definition for the 'authors' table.

Defines the Author entity and its relationship with Recipe.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.persistence.db import Base

class Author(Base):
    """
    SQLAlchemy model representing an author.

    Each author has a unique ID and email address.
    An author can be associated with multiple recipes.
    Deleting an author will also delete their associated recipes.
    """
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    # One-to-many relationship: an author can have many recipes
    # The cascade option ensures that when an Author is deleted,
    # all their associated recipes are also deleted
    recipes = relationship("Recipe", back_populates="author", cascade="all, delete-orphan")