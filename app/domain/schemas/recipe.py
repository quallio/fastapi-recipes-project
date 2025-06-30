from pydantic import BaseModel
from typing import List, Optional, Union

from app.domain.schemas.author import AuthorResponse


# ─────────────────────────────── BASE ───────────────────────────────
class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None


# ───────────── Ingredient structure inside a recipe ────────────────
class IngredientInRecipe(BaseModel):
    ingredient_id: int
    quantity: Union[int, float]
    unit: str

    class Config:
        orm_mode = True


# ─────────────────────────────── CREATE ─────────────────────────────
class RecipeCreate(RecipeBase):
    author_id: int
    ingredients: List[IngredientInRecipe]


# ─────────────────────────────── UPDATE ─────────────────────────────
class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    ingredients: Optional[List[IngredientInRecipe]] = None


# ─────────────────────────────── RESPONSE ───────────────────────────
class RecipeResponse(RecipeBase):
    id: int
    author: AuthorResponse
    ingredients: List[IngredientInRecipe]

    class Config:
        orm_mode = True
