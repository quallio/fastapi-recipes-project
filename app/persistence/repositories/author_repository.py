from typing import Optional, List
from sqlalchemy.orm import Session

from app.domain.models.author import Author
from app.domain.schemas.author import AuthorCreate
from app.persistence.repositories.base_repository import BaseRepository

class AuthorRepository(BaseRepository[Author]):
    def __init__(self):
        super().__init__(Author)

    def get_by_email(self, db: Session, email: str) -> Optional[Author]:
        return db.query(self.model).filter(self.model.email == email).first()

    def create_authors(self, db: Session, author_items: List[AuthorCreate]) -> List[Author]:
        authors = [Author(name=a.name, email=a.email) for a in author_items]
        db.add_all(authors)
        db.commit()
        for a in authors:
            db.refresh(a)
        return authors

    def update_author(
        self, db: Session, author: Author, *, name: Optional[str] = None, email: Optional[str] = None
    ) -> Author:
        if name is not None:
            author.name = name
        if email is not None:
            author.email = email
        db.add(author)
        db.commit()
        db.refresh(author)
        return author
