from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.models.recipe import Recipe
from app.domain.schemas.recipe import RecipeResponse, IngredientInRecipe
from app.application.exceptions.recipe_exceptions import (
    RecipeNotFoundError, RecipeAlreadyExistsError
)
from app.application.exceptions.author_exceptions import AuthorNotFoundError
from app.application.exceptions.ingredient_exceptions import IngredientNotFoundError
from app.persistence.repositories.recipe_repository import RecipeRepository
from app.persistence.repositories.author_repository import AuthorRepository
from app.persistence.repositories.ingredient_repository import IngredientRepository


class RecipeService:
    def __init__(self, db: Session):
        self.db = db
        self.recipe_repo = RecipeRepository()
        self.author_repo = AuthorRepository()
        self.ingredient_repo = IngredientRepository()


    # ─────────────── PRIVATE HELPERS ───────────────

    def _validate_ingredients_exist(self, ingredient_ids: List[int]) -> None:
        existing = self.ingredient_repo.get_existing_ids(self.db, ingredient_ids)
        missing = list(set(ingredient_ids) - existing)
        if missing:
            raise IngredientNotFoundError(missing)

    def _build_id_to_name_map(self, ingredient_ids: list[int]) -> dict[int, str]:
        """
        Sólo consulta los ingredientes de esta receta,
        evitando traer todo el catálogo.
        """
        return self.ingredient_repo.get_id_name_map_by_ids(self.db, ingredient_ids)
    

    # ─────────────── CREATE ───────────────
    def create_recipe(
        self,
        *,
        title: str,
        description: Optional[str],
        author_id: int,
        ingredients_data: List[dict],
    ) -> Recipe:
        # 1) Un único query para ver si ya existe
        if self.recipe_repo.get_by_title(self.db, title):
            raise RecipeAlreadyExistsError(title)

        # 2) Validar autor
        if self.author_repo.get_by_id(self.db, author_id) is None:
            raise AuthorNotFoundError(author_id)

        # 3) Validar ingredientes
        ingredient_ids = [i["ingredient_id"] for i in ingredients_data]
        self._validate_ingredients_exist(ingredient_ids)

        # 4) Delegar creación
        return self.recipe_repo.create(
            self.db,
            title=title,
            description=description,
            author_id=author_id,
            ingredients_data=ingredients_data,
        )

    # ─────────────── READ ────────────────
    def get_recipe(self, recipe_id: int) -> RecipeResponse:
        recipe = self.recipe_repo.get_by_id(self.db, recipe_id)
        if recipe is None:
            raise RecipeNotFoundError(recipe_id)

        # 1) Extraer solo los IDs de los ingredientes de esta receta
        ingredient_ids = [ri.ingredient_id for ri in recipe.ingredients]

        # 2) Construir el map solo para esos IDs
        id_to_name = self._build_id_to_name_map(ingredient_ids)

        # 3) Enriquecer la lista con nombres
        enriched = [
            IngredientInRecipe(
                ingredient_id=ri.ingredient_id,
                quantity=ri.quantity,
                unit=ri.unit,
                ingredient_name=id_to_name.get(ri.ingredient_id),
            )
            for ri in recipe.ingredients
        ]

        # 4) Devolver el response
        return RecipeResponse(
            id=recipe.id,
            title=recipe.title,
            description=recipe.description,
            author=recipe.author,
            ingredients=enriched,
        )
    
    # ─────────────── READ LIST ────────────────
    def list_recipes(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[RecipeResponse]:
        recipes = self.recipe_repo.list(self.db, skip=skip, limit=limit)
        response: List[RecipeResponse] = []

        for r in recipes:
            ingredient_ids = [ri.ingredient_id for ri in r.ingredients]
            id_to_name = self._build_id_to_name_map(ingredient_ids)
            enriched = [
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
                    ingredients=enriched,
                )
            )
        return response

    # ─────────────── UPDATE ────────────────
    def update_recipe(
        self,
        recipe_id: int,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        ingredients_data: Optional[List[dict]] = None
    ) -> RecipeResponse:
        recipe = self.recipe_repo.get_by_id(self.db, recipe_id)
        if recipe is None:
            raise RecipeNotFoundError(recipe_id)

        if ingredients_data is not None:
            ingredient_ids = [i["ingredient_id"] for i in ingredients_data]
            self._validate_ingredients_exist(ingredient_ids)

        updated = self.recipe_repo.update_recipe(
            self.db,
            recipe,
            title=title,
            description=description,
            ingredients_data=ingredients_data
        )

        # Reusar get_recipe para formatear la respuesta
        return self.get_recipe(updated.id)

    # ─────────────── DELETE ────────────────
    def delete_recipe(self, recipe_id: int) -> None:
        recipe = self.recipe_repo.get_by_id(self.db, recipe_id)
        if recipe is None:
            raise RecipeNotFoundError(recipe_id)
        self.recipe_repo.delete(self.db, recipe)
