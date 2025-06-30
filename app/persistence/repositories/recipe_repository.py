"""
Repository layer for Recipe entity.

This module contains all low-level database operations related to Recipe,
encapsulating direct SQLAlchemy usage from the rest of the application.
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.models.recipe import Recipe
from app.domain.models.recipe_ingredient import RecipeIngredient


def create_recipe(
    db: Session,
    *,
    title: str,
    description: Optional[str],
    author_id: int,
    ingredients_data: List[dict]
) -> Recipe:
    """
    Insert a new Recipe into the database with its ingredients.

    Args:
        db: Database session.
        title: Recipe title.
        description: Optional description.
        author_id: ID of the author.
        ingredients_data: List of dicts with ingredient_id, quantity, and unit.

    Returns:
        The newly created Recipe instance.
    """
    recipe = Recipe(title=title, description=description, author_id=author_id)

    for item in ingredients_data:
        ri = RecipeIngredient(
            ingredient_id=item["ingredient_id"],
            quantity=item["quantity"],
            unit=item["unit"],
        )
        recipe.ingredients.append(ri)

    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe


def get_recipe_by_id(db: Session, recipe_id: int) -> Optional[Recipe]:
    """
    Retrieve a Recipe by its primary key.

    Args:
        db: Database session.
        recipe_id: Recipe's unique ID.

    Returns:
        The Recipe if found, otherwise None.
    """
    return db.get(Recipe, recipe_id)


def list_recipes(db: Session, *, skip: int = 0, limit: int = 100) -> List[Recipe]:
    """
    Return a paginated list of recipes.

    Args:
        db: Database session.
        skip: Number of records to skip.
        limit: Maximum number of records to return.

    Returns:
        A list of Recipe instances.
    """
    return db.query(Recipe).offset(skip).limit(limit).all()


def update_recipe(
    db: Session,
    recipe: Recipe,
    *,
    title: Optional[str] = None,
    description: Optional[str] = None,
    ingredients_data: Optional[List[dict]] = None
) -> Recipe:
    """
    Update an existing Recipe instance and optionally replace its ingredients.

    Args:
        db: Database session.
        recipe: The Recipe to update (already loaded from DB).
        title: New title (optional).
        description: New description (optional).
        ingredients_data: New list of ingredients (optional).

    Returns:
        The updated Recipe instance.
    """
    if title is not None:
        recipe.title = title
    if description is not None:
        recipe.description = description

    if ingredients_data is not None:
        recipe.ingredients.clear()
        for item in ingredients_data:
            ri = RecipeIngredient(
                ingredient_id=item["ingredient_id"],
                quantity=item["quantity"],
                unit=item["unit"],
            )
            recipe.ingredients.append(ri)

    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe


def delete_recipe(db: Session, recipe: Recipe) -> None:
    """
    Delete an existing Recipe from the database.

    Args:
        db: Database session.
        recipe: The Recipe to delete.

    Returns:
        None
    """
    db.delete(recipe)
    db.commit()
