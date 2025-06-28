"""
Seed the database with a minimal but consistent dataset.

This script creates two authors, four ingredients, two recipes and the
associated many‑to‑many entries in recipe_ingredients, linking everything
by objects instead of explicit foreign‑key IDs.

Run inside the running API container:

docker-compose exec api python -m scripts.seed_data
"""

from sqlalchemy.orm import Session

from app.persistence.db import SessionLocal
from app.domain.models import (
    Author,
    Ingredient,
    Recipe,
    RecipeIngredient,
)


def seed_data() -> None:
    """Populate the database using object relationships (no manual ID handling)."""
    db: Session = SessionLocal()

    try:
        # ── Authors ──────────────────────────────────────────────────────
        author_juan = Author(name="Juan Pérez", email="juan@example.com")
        author_ana = Author(name="Ana Gómez", email="ana@example.com")

        # ── Ingredients ─────────────────────────────────────────────────
        ing_flour = Ingredient(name="Flour")
        ing_eggs = Ingredient(name="Eggs")
        ing_milk = Ingredient(name="Milk")
        ing_sugar = Ingredient(name="Sugar")

        # ── Recipes linked via Author objects ───────────────────────────
        recipe_pancakes = Recipe(
            title="Pancakes",
            description="Classic pancakes with milk and eggs.",
            author=author_juan,
        )
        recipe_cake = Recipe(
            title="Cake",
            description="Sweet cake with flour and sugar.",
            author=author_ana,
        )

        # ── Link ingredients to recipes through RecipeIngredient objects ─
        recipe_pancakes.ingredients.extend(
            [
                RecipeIngredient(ingredient=ing_flour, quantity=200, unit="g"),
                RecipeIngredient(ingredient=ing_eggs, quantity=2, unit="pcs"),
                RecipeIngredient(ingredient=ing_milk, quantity=250, unit="ml"),
            ]
        )
        recipe_cake.ingredients.extend(
            [
                RecipeIngredient(ingredient=ing_flour, quantity=300, unit="g"),
                RecipeIngredient(ingredient=ing_sugar, quantity=100, unit="g"),
            ]
        )

        # ── Persist all objects in a single transaction ─────────────────
        db.add_all(
            [
                author_juan,
                author_ana,
                ing_flour,
                ing_eggs,
                ing_milk,
                ing_sugar,
                recipe_pancakes,
                recipe_cake,
            ]
        )
        db.commit()
        print("Seed data inserted successfully")

    except Exception as e:
        db.rollback()
        print("Error seeding data:", e)
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
