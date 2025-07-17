"""
HTTP routes for the Recipe entity.

Exposes REST-style endpoints to create, read, update and delete recipes.
"""

from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.persistence.db import get_db

from app.domain.schemas.recipe import (
    RecipeCreate,
    RecipeUpdate,
    RecipeResponse,
)

from app.application.services.recipe_service import (
    create_recipe_service,
    get_recipe_service,
    list_recipes_service,
    update_recipe_service,
    delete_recipe_service,
)


router = APIRouter(prefix="/recipes", tags=["Recipes"])

# ─────────────────────────────── CREATE ──────────────────────────────
@router.post(
    "/",
    response_model=RecipeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new recipe (with ingredients)",
)
def create_recipe(
    recipe_in: RecipeCreate,
    db: Session = Depends(get_db),
):
    """
    Persist a new recipe together with its ingredient list.

    * **404** – Author or any ingredient does not exist
    """

    return create_recipe_service(
        db,
        title=recipe_in.title,
        description=recipe_in.description,
        author_id=recipe_in.author_id,
        ingredients_data=[i.model_dump() for i in recipe_in.ingredients],
    )


# ─────────────────────────────── LIST ────────────────────────────────
@router.get(
    "/",
    response_model=List[RecipeResponse],
    status_code=status.HTTP_200_OK,
    summary="List recipes (paginated)",
)
def list_recipes(
    skip: int = Query(0, ge=0, description="Records to skip"),
    limit: int = Query(100, gt=0, le=500, description="Page size"),
    db: Session = Depends(get_db),
):
    """Return a paginated list of recipes."""
    return list_recipes_service(db, skip=skip, limit=limit)


# ─────────────────────────────── RETRIEVE ────────────────────────────
@router.get(
    "/{recipe_id}",
    response_model=RecipeResponse,
    status_code=status.HTTP_200_OK,
    summary="Get recipe by ID",
)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """
    Fetch a single recipe.
 
    * **404** – Recipe not found
    """
    return get_recipe_service(db, recipe_id)

# ─────────────────────────────── UPDATE ──────────────────────────────
@router.put(
    "/{recipe_id}",
    response_model=RecipeResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a recipe (title/description/ingredients)",
)
def update_recipe(
    recipe_id: int,
    recipe_in: RecipeUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing recipe.

    * **404** – Recipe, author or ingredient not found
    """
    return update_recipe_service(
        db,
        recipe_id,
        title=recipe_in.title,
        description=recipe_in.description,
        ingredients_data=(
            [i.model_dump() for i in recipe_in.ingredients]
            if recipe_in.ingredients is not None
            else None
        ),
    )

# ─────────────────────────────── DELETE ──────────────────────────────
@router.delete(
    "/{recipe_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a recipe",
)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """
    Delete a recipe.

    * **404** – Recipe not found
    """
    delete_recipe_service(db, recipe_id)
    return