"""
SQLAlchemy model definition for the 'recipes' table.

Defines the Recipe entity and its relationships with Author and RecipeIngredient.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.persistence.db import Base

class Recipe(Base):
    """
    SQLAlchemy model representing a recipe.

    Each recipe has a title, optional description, creation timestamp,
    and is authored by a registered user (Author).
    A recipe contains multiple ingredients through the RecipeIngredient association table.
    """
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # One-to-many relationship: a recipe includes multiple ingredients.
    # Cascade ensures that deleting a recipe also deletes its associated entries in the association table.
    ingredients = relationship(
        "RecipeIngredient",
        back_populates="recipe",
        cascade="all, delete-orphan"
    )

    # Many-to-one relationship: each recipe is linked to one author.
    author = relationship("Author", back_populates="recipes")
