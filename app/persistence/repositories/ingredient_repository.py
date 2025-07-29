from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.models.ingredient import Ingredient
from app.persistence.repositories.base_repository import BaseRepository


class IngredientRepository(BaseRepository[Ingredient]):
    def __init__(self):
        super().__init__(Ingredient)

    def get_by_name(self, db: Session, name: str) -> Optional[Ingredient]:
        return db.query(self.model).filter(self.model.name == name).first()

    def create(self, db: Session, name: str) -> Ingredient:
        ingredient = Ingredient(name=name)
        db.add(ingredient)
        db.commit()
        db.refresh(ingredient)
        return ingredient

    def get_existing_ids(self, db: Session, ids: List[int]) -> set[int]:
        """
        Return the subset of the given IDs that actually exist in the ingredients table.

        Args:
            db: Database session.
            ids: List of ingredient IDs to check.

        Returns:
            A set of IDs that were found in the DB.
        """
        rows = (
            db.query(self.model.id)
              .filter(self.model.id.in_(ids))
              .all()
        )
        return {row.id for row in rows}

    def get_id_name_map_by_ids(
        self,
        db: Session,
        ids: list[int]
    ) -> dict[int, str]:
        """
        Return a mapping {ingredient_id: ingredient_name}
        only for the given list of IDs.
        """
        rows = (
            db.query(self.model.id, self.model.name)
              .filter(self.model.id.in_(ids))
              .all()
        )
        return {row.id: row.name for row in rows}
    
    # def bulk_create(self, 
    #                 db: Session, 
    #                 names: list[str]
    #                 ) -> list[Ingredient]:
    #     """
    #     Creates multiple Ingredient objects in one bulk operation.
    #     """
    #     objs = [Ingredient(name=name) for name in names]
    #     db.bulk_save_objects(objs)
    #     db.commit()
    #     # bulk_save_objects does not refresh the PKs, so we refresh:
    #     for obj in objs:
    #         db.refresh(obj)
    #     return objs
    
    def bulk_create(self, db: Session, names: List[str]) -> List[Ingredient]:
        """
        Create multiple ingredients in one operation.
        Uses ORM add_all for simplicity and automatic id propagation.
        """
        # Build Ingredient instances
        objs = [Ingredient(name=name) for name in names]
        # Add all to the session
        db.add_all(objs)
        # Flush and commit will populate ids automatically
        db.commit()
        return objs