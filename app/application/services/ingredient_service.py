import csv
import io
from typing import List

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.domain.models.ingredient import Ingredient
from app.domain.models.recipe_ingredient import RecipeIngredient
from app.domain.schemas.ingredient import IngredientImportItem
from app.application.exceptions.ingredient_exceptions import (
    IngredientAlreadyExistsError,
    IngredientNotFoundError,
    IngredientInUseError,
    InvalidCSVError,
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

    # ─────────────── BULK IMPORT ───────────────
    async def bulk_import(self, file: UploadFile) -> List[IngredientImportItem]:
        """
        Read CSV from the uploaded file, validate and bulk-insert new ingredients.
        Returns a report per row with name, status and new id if created.
        """
        if not file.filename.lower().endswith(".csv"):
            raise InvalidCSVError("Uploaded file is not a .csv")

        content = await file.read()
        # reader = csv.DictReader(io.StringIO(content.decode('utf-8')))
        text = content.decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(text))

        seen = set()
        to_create = []
        report: List[IngredientImportItem] = []

        for row in reader:
            name = row.get("name", "").strip()
            if not name:
                report.append(IngredientImportItem(name=name, status="error: missing name"))
                continue
            if name in seen:
                report.append(IngredientImportItem(name=name, status="skipped: duplicate in file"))
                continue
            seen.add(name)
            existing = self.repo.get_by_name(self.db, name)
            if existing:
                report.append(
                    IngredientImportItem(
                        name=name,
                        status="skipped: already exists",
                        id=existing.id
                    )
                )
            else:
                to_create.append(name)

        # Bulk create new ingredients via repo.bulk_create (uses add_all())
        if to_create:
            created = self.repo.bulk_create(self.db, to_create)
            for ing in created:
                report.append(
                    IngredientImportItem(name=ing.name, status="created", id=ing.id)
                )

        return report
