from pydantic import BaseModel
from typing import Optional, List

from app.domain.schemas.ingredient import IngredientRead


class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None


class RecipeCreate(RecipeBase):
    author_id: int
    ingredients: List[int]


class RecipeRead(RecipeBase):
    id: int
    ingredients: List[IngredientRead]

    class Config:
        orm_mode = True
