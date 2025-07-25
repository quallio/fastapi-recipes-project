from fastapi import Depends
from sqlalchemy.orm import Session

from app.persistence.db import get_db
from app.application.services.user_service import UserService

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """
    Dependency provider for UserService: inyecta la sesión de DB
    y devuelve la instancia de servicio.
    """
    return UserService(db)
