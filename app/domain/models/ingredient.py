"""
SQLAlchemy model definition for the 'ingredients' table.

Defines the Ingredient entity and its relationship with RecipeIngredient.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.persistence.db import Base

class Ingredient(Base):
    """
    SQLAlchemy model representing an ingredient.

    Each ingredient has a unique ID and a unique name.
    An ingredient can be used in many recipes through the RecipeIngredient association table.
    Deletion of an ingredient that is still in use by recipes is not allowed.
    """
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # One-to-many relationship with the association table RecipeIngredient.
    # No cascade: deletion is restricted if the ingredient is still used in recipes.
    recipe_ingredients = relationship("RecipeIngredient", back_populates="ingredient")