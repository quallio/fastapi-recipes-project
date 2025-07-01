"""
SQLAlchemy model definition for the 'recipe_ingredients' association table.

This table represents the many-to-many relationship between recipes and ingredients,
including additional information such as quantity and unit.
"""

from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.persistence.db import Base

class RecipeIngredient(Base):
    """
    SQLAlchemy model for the association between Recipe and Ingredient.

    This table includes:
    - Foreign keys to both Recipe and Ingredient.
    - Quantity and unit of each ingredient used in a recipe.
    Acts as a join table with extra data.
    """
    __tablename__ = "recipe_ingredients"

    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), primary_key=True)
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)

    # Many-to-one relationship to the Recipe this entry belongs to.
    recipe = relationship("Recipe", back_populates="ingredients")

    # Many-to-one relationship to the Ingredient used in the recipe.
    ingredient = relationship("Ingredient", back_populates="recipe_ingredients")
