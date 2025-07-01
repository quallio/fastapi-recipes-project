from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Union

from app.domain.schemas.author import AuthorResponse

# ─────────────────────────────── BASE ───────────────────────────────
class RecipeBase(BaseModel):
    title: str = Field(..., example="Spaghetti Carbonara")
    description: Optional[str] = Field(None, example="A classic Roman pasta dish.")


# ───────────── Ingredient structure inside a recipe ────────────────
class IngredientInRecipe(BaseModel):
    ingredient_id: int = Field(..., example=1)
    quantity: Union[int, float] = Field(..., example=200)
    unit: str = Field(..., example="grams")
    ingredient_name: Optional[str] = Field(None, example="Sugar")


    model_config = ConfigDict(from_attributes=True)


# ─────────────────────────────── CREATE ─────────────────────────────
class RecipeCreate(RecipeBase):
    author_id: int = Field(..., example=1)
    ingredients: List[IngredientInRecipe] = Field(
        ...,
        example=[
            {"ingredient_id": 1, "quantity": 200, "unit": "grams"},
            {"ingredient_id": 2, "quantity": 100, "unit": "ml"},
        ],
    )


# ─────────────────────────────── UPDATE ─────────────────────────────
class RecipeUpdate(BaseModel):
    title: Optional[str] = Field(None, example="Updated Pasta Title")
    description: Optional[str] = Field(None, example="Updated recipe description.")
    ingredients: Optional[List[IngredientInRecipe]] = Field(
        None,
        example=[
            {"ingredient_id": 1, "quantity": 250, "unit": "grams"},
            {"ingredient_id": 3, "quantity": 50, "unit": "ml"},
        ],
    )


# ─────────────────────────────── RESPONSE ───────────────────────────
class RecipeResponse(RecipeBase):
    id: int
    author: AuthorResponse
    ingredients: List[IngredientInRecipe]

    model_config = ConfigDict(from_attributes=True)
