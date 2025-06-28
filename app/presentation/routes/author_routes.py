"""
HTTP routes for the Author entity.

Exposes RESTful endpoints to create, read, update and delete authors.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.application.services.author_service import (
    create_author_service,
    get_author_service,
    list_authors_service,
    update_author_service,
    delete_author_service,
)
from app.application.exceptions.author_exceptions import (
    AuthorAlreadyExistsError,
    AuthorNotFoundError,
)
from app.domain.schemas.author import AuthorCreate, AuthorResponse, AuthorUpdate
from app.persistence.db import get_db

router = APIRouter(prefix="/authors", tags=["Authors"])

# ─────────────────────────────── CREATE ──────────────────────────────
@router.post(
    "/",
    response_model=AuthorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new author",
)
def create_author(author_in: AuthorCreate, db: Session = Depends(get_db)):
    """
    Create a new author with a unique email.
    Returns 409 Conflict if that email already exists.
    """
    try:
        return create_author_service(db, name=author_in.name, email=author_in.email)
    except AuthorAlreadyExistsError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


# ─────────────────────────────── READ ONE ────────────────────────────
@router.get(
    "/{author_id}",
    response_model=AuthorResponse,
    status_code=status.HTTP_200_OK,
    summary="Get an author by ID",
)
def read_author(author_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single author by primary key.
    Returns 404 if the author does not exist.
    """
    try:
        return get_author_service(db, author_id)
    except AuthorNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


# ─────────────────────────────── READ LIST ───────────────────────────
@router.get(
    "/",
    response_model=List[AuthorResponse],
    status_code=status.HTTP_200_OK,
    summary="List authors (paginated)",
)
def list_authors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Return a paginated list of authors.
    """
    return list_authors_service(db, skip=skip, limit=limit)


# ─────────────────────────────── DELETE ──────────────────────────────
@router.delete(
    "/{author_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an author",
)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    """
    Delete an author by ID. Returns 204 No Content on success.
    """
    try:
        delete_author_service(db, author_id)
    except AuthorNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


# ─────────────────────────────── UPDATE ──────────────────────────────
@router.put("/{author_id}", response_model=AuthorResponse, status_code=200)
def update_author(
    author_id: int,
    author_in: AuthorUpdate,
    db: Session = Depends(get_db),
):
    try:
        return update_author_service(
            db,
            author_id,
            name=author_in.name,
            email=author_in.email,
        )
    except AuthorAlreadyExistsError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except AuthorNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
