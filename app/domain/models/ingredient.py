from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.persistence.db import Base

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # Relationship to the association table
    # No cascade: we want to prevent deletion if still related
    recipe_ingredients = relationship("RecipeIngredient", back_populates="ingredient")
