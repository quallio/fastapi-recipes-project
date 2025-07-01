"""
Service layer for Recipe entity.

This module contains business logic for managing recipes,
including ingredient validation and delegation to the repository layer.
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.models.ingredient import Ingredient
from app.persistence.repositories import (
    recipe_repository,
    author_repository,
    ingredient_repository,
)

from app.domain.schemas.recipe import RecipeResponse, IngredientInRecipe
from app.application.exceptions.recipe_exceptions import RecipeNotFoundError
from app.application.exceptions.ingredient_exceptions import IngredientNotFoundError
from app.application.exceptions.author_exceptions import AuthorNotFoundError


def _validate_ingredients_exist(db: Session, ingredient_ids: List[int]) -> None:
    """Helper: ensure every ID in 'ingredient_ids' exists in the DB."""
    if not ingredient_ids:
        return

    found_ids = (
        db.query(Ingredient.id)
        .filter(Ingredient.id.in_(ingredient_ids))
        .all()
    )
    found_ids = {row.id for row in found_ids} # set comprehension. 

    for ing_id in ingredient_ids:
        if ing_id not in found_ids:
            raise IngredientNotFoundError(ing_id)


def _build_id_to_name_map(db: Session) -> dict[int, str]:
    """Helper: returns a mapping from ingredient_id to name."""
    ingredients = ingredient_repository.list_ingredients(db, skip=0, limit=10000)
    return {ing.id: ing.name for ing in ingredients}


# ───────────────────────── CREATE ──────────────────────────
def create_recipe_service(
    db: Session,
    *,
    title: str,
    description: Optional[str],
    author_id: int,
    ingredients_data: List[dict],
):
    """
    Business flow to create a recipe.

    1. Ensure author exists.
    2. Ensure every ingredient_id in `ingredients_data` exists.
    3. Delegate insert to repository.
    """
    author = author_repository.get_author_by_id(db, author_id)
    if author is None:
        raise AuthorNotFoundError(author_id=author_id)

    ingredient_ids = [item["ingredient_id"] for item in ingredients_data]
    _validate_ingredients_exist(db, ingredient_ids)

    return recipe_repository.create_recipe(
        db,
        title=title,
        description=description,
        author_id=author_id,
        ingredients_data=ingredients_data,
    )


# ───────────────────────── READ ────────────────────────────
def get_recipe_service(db: Session, recipe_id: int):
    recipe = recipe_repository.get_recipe_by_id(db, recipe_id)
    if recipe is None:
        raise RecipeNotFoundError(recipe_id)

    id_to_name = _build_id_to_name_map(db)
    enriched_ingredients = [
        IngredientInRecipe(
            ingredient_id=ri.ingredient_id,
            quantity=ri.quantity,
            unit=ri.unit,
            ingredient_name=id_to_name.get(ri.ingredient_id),
        )
        for ri in recipe.ingredients
    ]

    return RecipeResponse(
        id=recipe.id,
        title=recipe.title,
        description=recipe.description,
        author=recipe.author,
        ingredients=enriched_ingredients,
    )


def list_recipes_service(db: Session, *, skip: int = 0, limit: int = 100):
    recipes = recipe_repository.list_recipes(db, skip=skip, limit=limit)
    id_to_name = _build_id_to_name_map(db)

    response: List[RecipeResponse] = []
    for r in recipes:
        enriched_ingredients = [
            IngredientInRecipe(
                ingredient_id=ri.ingredient_id,
                quantity=ri.quantity,
                unit=ri.unit,
                ingredient_name=id_to_name.get(ri.ingredient_id),
            )
            for ri in r.ingredients
        ]

        response.append(
            RecipeResponse(
                id=r.id,
                title=r.title,
                description=r.description,
                author=r.author,
                ingredients=enriched_ingredients,
            )
        )
    return response


# ───────────────────────── UPDATE ──────────────────────────
def update_recipe_service(
    db: Session,
    recipe_id: int,
    *,
    title: Optional[str] = None,
    description: Optional[str] = None,
    ingredients_data: Optional[List[dict]] = None,
):
    """
    Update a recipe and, if provided, replace its ingredient list.
    """
    recipe = recipe_repository.get_recipe_by_id(db, recipe_id)
    if recipe is None:
        raise RecipeNotFoundError(recipe_id)

    # Validate new ingredients only if caller sent a new list
    if ingredients_data is not None:
        ingredient_ids = [i["ingredient_id"] for i in ingredients_data]
        _validate_ingredients_exist(db, ingredient_ids)

    return recipe_repository.update_recipe(
        db,
        recipe,
        title=title,
        description=description,
        ingredients_data=ingredients_data,
    )


# ───────────────────────── DELETE ──────────────────────────
def delete_recipe_service(db: Session, recipe_id: int) -> None:
    recipe = recipe_repository.get_recipe_by_id(db, recipe_id)
    if recipe is None:
        raise RecipeNotFoundError(recipe_id)

    recipe_repository.delete_recipe(db, recipe)