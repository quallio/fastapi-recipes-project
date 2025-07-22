from fastapi import Depends
from sqlalchemy.orm import Session

from app.persistence.db import get_db
from app.application.services.author_service import AuthorService

def get_author_service(db: Session = Depends(get_db)) -> AuthorService:
    return AuthorService(db)
