"""
Repository layer for Author entity.

This module contains all low-level database operations related to Author,
encapsulating direct SQLAlchemy usage from the rest of the application.
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.models.author import Author
from app.domain.schemas.author import AuthorCreate

# POST Authors endpoint is not using this fn at the moment.
def create_author(db: Session, *, name: str, email: str) -> Author:
    """
    Insert a new Author into the database.

    Args:
        db: Database session.
        name: Author's full name.
        email: Author's email address.

    Returns:
        The newly created Author instance.
    """
    author = Author(name=name, email=email)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


# POST Authors endpoint is using this fn.
def create_authors(
    db: Session,
    author_items: List[AuthorCreate],
) -> List[Author]:
    """
    Insert multiple Authors with a single transaction.

    Args:
        db: Database session.
        authors_data: List of AuthorsCreate, each containing .name and .email.

    Returns:
        List of newly created Author instances.
    """
    authors_created: List[Author] = []

    for data in author_items:
        author = Author(name=data.name, email=data.email)
        db.add(author)
        authors_created.append(author)

    db.commit()                 # one commit for all the authors created
    for author in authors_created:
        db.refresh(author)

    return authors_created


def get_author_by_id(db: Session, author_id: int) -> Optional[Author]:
    """
    Retrieve an Author by its primary key.

    Args:
        db: Database session.
        author_id: Author's unique ID.

    Returns:
        The Author if found, otherwise None.
    """
    return db.get(Author, author_id)


def get_author_by_email(db: Session, email: str) -> Optional[Author]:
    """
    Retrieve an Author by their unique email address.

    Args:
        db: Database session.
        email: Author's email.

    Returns:
        The Author if found, otherwise None.
    """
    return db.query(Author).filter(Author.email == email).first()


def list_authors(db: Session, *, skip: int = 0, limit: int = 100) -> List[Author]:
    """
    Return a paginated list of authors.

    Args:
        db: Database session.
        skip: Number of records to skip.
        limit: Maximum number of records to return.

    Returns:
        A list of Author instances.
    """
    return db.query(Author).offset(skip).limit(limit).all()


def update_author(
    db: Session,
    author: Author,
    *,
    name: Optional[str] = None,
    email: Optional[str] = None,
) -> Author:
    """
    Update an existing Author instance.

    Args:
        db: Database session.
        author: The Author to update (already loaded from DB).
        name: New name (optional).
        email: New email (optional).

    Returns:
        The updated Author instance.
    """
    if name is not None:
        author.name = name
    if email is not None:
        author.email = email

    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def delete_author(db: Session, author: Author) -> None:
    """
    Delete an existing Author from the database.

    Args:
        db: Database session.
        author: The Author to delete.

    Returns:
        None
    """
    db.delete(author)
    db.commit()
