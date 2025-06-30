"""
Service layer for Ingredient entity.

This module contains business logic related to ingredients, and interacts
with the repository layer to perform DB operations.
"""

from typing import List
from sqlalchemy.orm import Session

from app.domain.models.ingredient import Ingredient
from app.domain.models.recipe_ingredient import RecipeIngredient
from app.persistence.repositories import ingredient_repository
from app.application.exceptions.ingredient_exceptions import (
    IngredientAlreadyExistsError,
    IngredientNotFoundError,
    IngredientInUseError,
)


# ───────────────────────── CREATE ─────────────────────────
def create_ingredient_service(db: Session, *, name: str) -> Ingredient:
    if ingredient_repository.get_ingredient_by_name(db, name):
        raise IngredientAlreadyExistsError(name)
    return ingredient_repository.create_ingredient(db, name=name)


# ───────────────────────── READ ──────────────────────────
def get_ingredient_service(db: Session, ingredient_id: int) -> Ingredient:
    ingredient = ingredient_repository.get_ingredient_by_id(db, ingredient_id)
    if ingredient is None:
        raise IngredientNotFoundError(ingredient_id)
    return ingredient


def list_ingredients_service(db: Session, skip: int = 0, limit: int = 100) -> List[Ingredient]:
    return ingredient_repository.list_ingredients(db, skip=skip, limit=limit)


# ───────────────────────── DELETE ────────────────────────
def delete_ingredient_service(db: Session, ingredient_id: int) -> None:
    ingredient = ingredient_repository.get_ingredient_by_id(db, ingredient_id)
    if ingredient is None:
        raise IngredientNotFoundError(ingredient_id)

    in_use = db.query(RecipeIngredient).filter_by(ingredient_id=ingredient_id).first()
    if in_use:
        raise IngredientInUseError(ingredient_id)

    ingredient_repository.delete_ingredient(db, ingredient)
