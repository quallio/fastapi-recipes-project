from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.models.recipe import Recipe
from app.domain.models.recipe_ingredient import RecipeIngredient
from app.persistence.repositories.base_repository import BaseRepository


class RecipeRepository(BaseRepository[Recipe]):
    def __init__(self):
        super().__init__(Recipe)

    def get_by_title(self, db: Session, title: str) -> Optional[Recipe]:
        """
        Retrieve a Recipe by its title.

        Args:
            db: Database session.
            title: Title of the recipe.

        Returns:
            The Recipe if found, otherwise None.
        """
        return db.query(self.model).filter_by(title=title).first()

    def create(
        self,
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

    def update_recipe(
        self,
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
