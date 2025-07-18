from fastapi import Depends
from sqlalchemy.orm import Session

from app.persistence.db import get_db
from app.application.services.ingredient_service import IngredientService

def get_ingredient_service(db: Session = Depends(get_db)) -> IngredientService:
    return IngredientService(db)
