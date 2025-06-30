"""
HTTP routes for the Ingredient entity.

Exposes REST-style endpoints to create, read, and delete ingredients.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.persistence.db import get_db
from app.domain.schemas.ingredient import (
    IngredientCreate,
    IngredientResponse,
)
from app.application.services.ingredient_service import (
    create_ingredient_service,
    get_ingredient_service,
    list_ingredients_service,
    delete_ingredient_service,
)
from app.application.exceptions.ingredient_exceptions import (
    IngredientAlreadyExistsError,
    IngredientNotFoundError,
    IngredientInUseError,
)

router = APIRouter(prefix="/ingredients", tags=["Ingredients"])

# ───────────── CREATE ─────────────
@router.post(
    "/",
    response_model=IngredientResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new ingredient",
)
def create_ingredient(
    ingredient_in: IngredientCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_ingredient_service(db, name=ingredient_in.name)
    except IngredientAlreadyExistsError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


# ───────────── LIST ──────────────
@router.get(
    "/",
    response_model=list[IngredientResponse],
    summary="List ingredients (paginated)",
)
def list_ingredients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return list_ingredients_service(db, skip=skip, limit=limit)


# ───────────── READ ──────────────
@router.get(
    "/{ingredient_id}",
    response_model=IngredientResponse,
    summary="Get ingredient by ID",
)
def get_ingredient(
    ingredient_id: int,
    db: Session = Depends(get_db),
):
    try:
        return get_ingredient_service(db, ingredient_id)
    except IngredientNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


# ───────────── DELETE ────────────
@router.delete(
    "/{ingredient_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an ingredient (must not be in use)",
)
def delete_ingredient(
    ingredient_id: int,
    db: Session = Depends(get_db),
):
    try:
        delete_ingredient_service(db, ingredient_id)
    except IngredientNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except IngredientInUseError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
