"""
HTTP routes for the Ingredient entity.

Exposes REST-style endpoints to create, read, and delete ingredients.
"""

from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status

from app.application.services.auth import get_current_user, get_current_active_admin
from app.application.services.ingredient_service import IngredientService
from app.application.services.ingredient_service_provider import get_ingredient_service
from app.domain.schemas.ingredient import (
    IngredientCreate,
    IngredientResponse,
    IngredientImportItem,
)

router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredients"],
    dependencies=[Depends(get_current_user)],
    )

# ───────────── CREATE ─────────────
@router.post(
    "/",
    response_model=IngredientResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new ingredient",
    dependencies=[Depends(get_current_active_admin)],
)
def create_ingredient(
    ingredient_in: IngredientCreate,
    service: IngredientService = Depends(get_ingredient_service),
):
    return service.create_ingredient(name=ingredient_in.name)

# ───────────── LIST ──────────────
@router.get(
    "/",
    response_model=list[IngredientResponse],
    summary="List ingredients (paginated)",
)
def list_ingredients(
    skip: int = 0,
    limit: int = 100,
    service: IngredientService = Depends(get_ingredient_service),
):
    return service.list_ingredients(skip=skip, limit=limit)

# ───────────── READ ──────────────
@router.get(
    "/{ingredient_id}",
    response_model=IngredientResponse,
    summary="Get ingredient by ID",
)
def get_ingredient(
    ingredient_id: int,
    service: IngredientService = Depends(get_ingredient_service),
):
    return service.get_ingredient(ingredient_id)

# ───────────── DELETE ────────────
@router.delete(
    "/{ingredient_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an ingredient (must not be in use)",
    dependencies=[Depends(get_current_active_admin)],
)
def delete_ingredient(
    ingredient_id: int,
    service: IngredientService = Depends(get_ingredient_service),
):
    return service.delete_ingredient(ingredient_id)

# ───────────── IMPORT CV ────────────
@router.post(
    "/import",
    response_model=List[IngredientImportItem],
    status_code=status.HTTP_201_CREATED,
    summary="Bulk import ingredients from CSV (admin only)",
    dependencies=[Depends(get_current_active_admin)],
)
async def import_ingredients_csv(
    file: UploadFile = File(..., description="CSV file with a `name` column"),
    service: IngredientService = Depends(get_ingredient_service),
) -> List[IngredientImportItem]:
    return await service.bulk_import(file)
