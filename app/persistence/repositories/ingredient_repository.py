"""
Repository layer for Ingredient entity.

Encapsulates all low-level DB operations so upper layers
do not deal with raw SQLAlchemy queries.
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.models.ingredient import Ingredient


# ───────────────────────── CREATE ─────────────────────────
def create_ingredient(db: Session, *, name: str) -> Ingredient:
    """Insert a new Ingredient into the DB and return it."""
    ingredient = Ingredient(name=name)
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    return ingredient


# ───────────────────────── READ ──────────────────────────
def get_ingredient_by_id(db: Session, ingredient_id: int) -> Optional[Ingredient]:
    return db.get(Ingredient, ingredient_id)


def get_ingredient_by_name(db: Session, name: str) -> Optional[Ingredient]:
    return db.query(Ingredient).filter(Ingredient.name == name).first()


def list_ingredients(db: Session, *, skip: int = 0, limit: int = 100) -> List[Ingredient]:
    return db.query(Ingredient).offset(skip).limit(limit).all()


# ───────────────────────── DELETE ────────────────────────
def delete_ingredient(db: Session, ingredient: Ingredient) -> None:
    db.delete(ingredient)
    db.commit()
