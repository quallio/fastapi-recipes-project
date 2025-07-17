from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.models.author import Author
from app.domain.schemas.author import AuthorCreate
from app.application.exceptions.author_exceptions import AuthorAlreadyExistsError, AuthorNotFoundError
from app.persistence.repositories.author_repository import AuthorRepository


class AuthorService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = AuthorRepository()

    def create_authors(self, author_items: List[AuthorCreate]) -> List[Author]:
        # 1) Verificar si hay emails duplicados en el payload
        emails = [a.email for a in author_items]
        if len(set(emails)) != len(emails):
            raise AuthorAlreadyExistsError(email="Duplicated email in payload")

        # 2) Verificar si alguno ya existe en la base
        for email in emails:
            if self.repository.get_by_email(self.db, email):
                raise AuthorAlreadyExistsError(email=email)

        return self.repository.create_authors(self.db, author_items)

    def get_author(self, author_id: int) -> Author:
        author = self.repository.get_by_id(self.db, author_id)
        if author is None:
            raise AuthorNotFoundError(author_id=author_id)
        return author

    def list_authors(self, skip: int = 0, limit: int = 100) -> List[Author]:
        return self.repository.list(self.db, skip=skip, limit=limit)

    def update_author(
        self,
        author_id: int,
        *,
        name: Optional[str] = None,
        email: Optional[str] = None
    ) -> Author:
        author = self.repository.get_by_id(self.db, author_id)
        if author is None:
            raise AuthorNotFoundError(author_id=author_id)

        if email is not None:
            duplicate = self.repository.get_by_email(self.db, email)
            if duplicate and duplicate.id != author_id:
                raise AuthorAlreadyExistsError(email)

        return self.repository.update_author(self.db, author, name=name, email=email)

    def delete_author(self, author_id: int) -> None:
        author = self.repository.get_by_id(self.db, author_id)
        if author is None:
            raise AuthorNotFoundError(author_id=author_id)

        self.repository.delete(self.db, author)
