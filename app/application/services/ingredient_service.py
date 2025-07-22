from typing import List
from sqlalchemy.orm import Session

from app.domain.models.ingredient import Ingredient
from app.domain.models.recipe_ingredient import RecipeIngredient
from app.application.exceptions.ingredient_exceptions import (
    IngredientAlreadyExistsError,
    IngredientNotFoundError,
    IngredientInUseError,
)
from app.persistence.repositories.ingredient_repository import IngredientRepository


class IngredientService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = IngredientRepository()

    # ─────────────── CREATE ───────────────
    def create_ingredient(self, name: str) -> Ingredient:
        if self.repo.get_by_name(self.db, name):
            raise IngredientAlreadyExistsError(name)
        return self.repo.create(self.db, name=name)

    # ─────────────── READ ────────────────
    def get_ingredient(self, ingredient_id: int) -> Ingredient:
        ingredient = self.repo.get_by_id(self.db, ingredient_id)
        if ingredient is None:
            raise IngredientNotFoundError(ingredient_id)
        return ingredient

    def list_ingredients(self, skip: int = 0, limit: int = 100) -> List[Ingredient]:
        return self.repo.list(self.db, skip=skip, limit=limit)

    # ─────────────── DELETE ──────────────
    def delete_ingredient(self, ingredient_id: int) -> None:
        ingredient = self.repo.get_by_id(self.db, ingredient_id)
        if ingredient is None:
            raise IngredientNotFoundError(ingredient_id)

        in_use = self.db.query(RecipeIngredient).filter_by(ingredient_id=ingredient_id).first()
        if in_use:
            raise IngredientInUseError(ingredient_id)

        self.repo.delete(self.db, ingredient)
