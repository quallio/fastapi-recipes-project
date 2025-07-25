from fastapi import Depends
from sqlalchemy.orm import Session

from app.persistence.db import get_db
from app.application.services.recipe_service import RecipeService

def get_recipe_service(db: Session = Depends(get_db)) -> RecipeService:
    """
    Dependency provider for RecipeService: inyecta la sesión de DB
    y devuelve la instancia de servicio.
    """
    return RecipeService(db)
