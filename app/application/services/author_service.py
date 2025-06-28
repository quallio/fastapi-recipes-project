"""
Service layer for Author entity.

This module contains business logic related to authors, and interacts
with the repository layer to perform DB operations.
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.models.author import Author
from app.persistence.repositories import author_repository
from app.application.exceptions.author_exceptions import AuthorAlreadyExistsError, AuthorNotFoundError


def create_author_service(db: Session, *, name: str, email: str) -> Author:
    """
    Business logic to create a new author.
    Prevents duplicate emails.

    Raises:
        AuthorAlreadyExistsError: If an author with the same email already exists.
    """
    existing = author_repository.get_author_by_email(db, email)
    if existing:
        raise AuthorAlreadyExistsError(email=email)

    return author_repository.create_author(db, name=name, email=email)


def get_author_service(db: Session, author_id: int) -> Author:
    """
    Retrieve an author by ID, or raise if not found.

    Raises:
        AuthorNotFoundError: If no author with the given ID exists.
    """
    author = author_repository.get_author_by_id(db, author_id)
    if author is None:
        raise AuthorNotFoundError(author_id=author_id)
    return author


def list_authors_service(db: Session, skip: int = 0, limit: int = 100) -> List[Author]:
    """Return a paginated list of authors."""
    return author_repository.list_authors(db, skip=skip, limit=limit)


def update_author_service(
    db: Session,
    author_id: int,
    *,
    name: Optional[str] = None,
    email: Optional[str] = None
) -> Author:
    """
    Update an author. Raises if not found.

    Raises:
        AuthorNotFoundError: If the author doesn't exist.
    """
    author = author_repository.get_author_by_id(db, author_id)
    if author is None:
        raise AuthorNotFoundError(author_id=author_id)
    
    if email is not None:
        duplicate = author_repository.get_author_by_email(db, email)
        if duplicate and duplicate.id != author_id:
            raise AuthorAlreadyExistsError(email)

    return author_repository.update_author(db, author, name=name, email=email)


def delete_author_service(db: Session, author_id: int) -> None:
    """
    Delete an author by ID.

    Raises:
        AuthorNotFoundError: If the author doesn't exist.
    """
    author = author_repository.get_author_by_id(db, author_id)
    if author is None:
        raise AuthorNotFoundError(author_id=author_id)

    author_repository.delete_author(db, author)
