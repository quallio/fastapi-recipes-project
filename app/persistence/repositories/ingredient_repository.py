from sqlalchemy.orm import Session

from app.domain.models.ingredient import Ingredient
from app.persistence.repositories.base_repository import BaseRepository

class IngredientRepository(BaseRepository[Ingredient]):
    def __init__(self):
        super().__init__(Ingredient)
    
    def get_by_name(self, db: Session, name: str) -> Ingredient | None:
        return db.query(self.model).filter(self.model.name == name).first()

    def create(self, db: Session, name: str) -> Ingredient:
        ingredient = Ingredient(name=name)
        db.add(ingredient)
        db.commit()
        db.refresh(ingredient)
        return ingredient
