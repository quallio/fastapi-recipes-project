# pylint: disable=missing-function-docstring, redefined-outer-name, invalid-name, line-too-long


"""
Unit tests for app.application.services.author_service
------------------------------------------------------

The real author_repository is monkey-patched by a lightweight DummyAuthorRepo
so we can exercise the service layer without touching a real database.
"""

from __future__ import annotations

from typing import Dict, List

import pytest

from app.application.services.author_service import (
    create_authors_service,
    delete_author_service,
    get_author_service,
    list_authors_service,
    update_author_service,
)
from app.application.exceptions.author_exceptions import (
    AuthorAlreadyExistsError,
    AuthorNotFoundError,
)
from app.domain.schemas.author import AuthorCreate


# ───────────────────────────── Helpers ──────────────────────────────
class SimpleAuthor:  # Tiny stand-in for app.domain.models.author.Author
    def __init__(self, id_: int, name: str, email: str):
        self.id = id_
        self.name = name
        self.email = email

    # nice representation for asserts
    def __repr__(self):  # pragma: no cover
        return f"SimpleAuthor(id={self.id}, email={self.email})"


class DummyAuthorRepo:
    """
    Minimal in-memory replacement for author_repository.
    """

    def __init__(self, initial: Dict[int, SimpleAuthor] | None = None):
        self.storage: Dict[int, SimpleAuthor] = dict(initial or {})
        self._id_seq = max(self.storage.keys(), default=0)

    # ---------- repo methods used by the service ----------

    def get_author_by_email(self, _db, email: str):
        return next((a for a in self.storage.values() if a.email == email), None)

    def get_author_by_id(self, _db, author_id: int):
        return self.storage.get(author_id)

    def list_authors(self, _db, skip: int = 0, limit: int = 100):
        return list(self.storage.values())[skip : skip + limit]

    def create_authors(self, _db, items: List[AuthorCreate]):
        created = []
        for item in items:
            self._id_seq += 1
            author = SimpleAuthor(self._id_seq, item.name, item.email)
            self.storage[self._id_seq] = author
            created.append(author)
        return created

    def update_author(
        self, _db, author: SimpleAuthor, *, name: str | None, email: str | None
    ):
        if name:
            author.name = name
        if email:
            author.email = email
        return author

    def delete_author(self, _db, author: SimpleAuthor):
        self.storage.pop(author.id, None)


# ───────────────────────────── Fixtures ─────────────────────────────
@pytest.fixture
def dummy_db():
    """Placeholder for a Session object (not used in the dummy repo)."""
    return None

# It is not necessary to use FakeSession in this case since we don't need to test
# things like db.commit(), db.refresh(), etc... in this case dummy_db returns None, that´s enough.
# It would be more appropriate for testing repository methods or integration tests.


@pytest.fixture
def repo(monkeypatch):
    """
    Creates a fresh DummyAuthorRepo for each test and monkey-patches it
    into author_service.
    """

    def _factory(initial: Dict[int, SimpleAuthor] | None = None) -> DummyAuthorRepo:
        dummy = DummyAuthorRepo(initial)
        monkeypatch.setattr(
            "app.application.services.author_service.author_repository", dummy
        )
        return dummy

    return _factory


# ───────────────────────────── Test: create_authors_service ─────────
def test_create_authors_success(dummy_db, repo):
    repo()
    # repo() would have been enough, since dummy is not used in this test.
    # However, it's important to call repo() so that the monkey-patch is applied.
    # Otherwise, the service would use the real author_repository, which we don't want in a unit test.
    # This applies to all service-related tests.

    payload = [
        AuthorCreate(name="Alice", email="alice@mail.com"),
        AuthorCreate(name="Bob", email="bob@mail.com"),
    ]

    created = create_authors_service(dummy_db, payload)

    assert len(created) == 2
    assert {a.email for a in created} == {"alice@mail.com", "bob@mail.com"}


def test_create_authors_duplicate_payload(dummy_db, repo):
    repo()
    payload = [
        AuthorCreate(name="Alice", email="dup@mail.com"),
        AuthorCreate(name="Dup", email="dup@mail.com"),  # duplicate inside payload
    ]
    with pytest.raises(AuthorAlreadyExistsError):
        create_authors_service(dummy_db, payload)


def test_create_authors_duplicate_db(dummy_db, repo):
    # dup@mail.com already exists in "DB"
    existing = {1: SimpleAuthor(1, "Taken", "dup@mail.com")}
    repo(existing)

    payload = [AuthorCreate(name="Other", email="dup@mail.com")]
    with pytest.raises(AuthorAlreadyExistsError):
        create_authors_service(dummy_db, payload)


# ───────────────────────────── Test: get_author_service ─────────────
def test_get_author_success(dummy_db, repo):
    existing = {1: SimpleAuthor(1, "Saved", "saved@mail.com")}
    repo(existing)

    author = get_author_service(dummy_db, 1)
    assert author.email == "saved@mail.com"


def test_get_author_not_found(dummy_db, repo):
    repo()  # empty
    with pytest.raises(AuthorNotFoundError):
        get_author_service(dummy_db, 99)


# ───────────────────────────── Test: list_authors_service ───────────
def test_list_authors(dummy_db, repo):
    existing = {
        1: SimpleAuthor(1, "A", "a@mail.com"),
        2: SimpleAuthor(2, "B", "b@mail.com"),
    }
    repo(existing)

    authors = list_authors_service(dummy_db, skip=0, limit=10)
    assert len(authors) == 2
    assert {a.email for a in authors} == {"a@mail.com", "b@mail.com"}


# ───────────────────────────── Test: update_author_service ──────────
def test_update_author_success(dummy_db, repo):
    existing = {1: SimpleAuthor(1, "Old", "old@mail.com")}
    repo(existing)

    updated = update_author_service(
        dummy_db, 1, name="New Name", email="new@mail.com"
    )
    assert updated.name == "New Name"
    assert updated.email == "new@mail.com"


def test_update_author_not_found(dummy_db, repo):
    repo()
    with pytest.raises(AuthorNotFoundError):
        update_author_service(dummy_db, 2, name="X")


def test_update_author_duplicate_email(dummy_db, repo):
    existing = {
        1: SimpleAuthor(1, "A", "a@mail.com"),
        2: SimpleAuthor(2, "B", "b@mail.com"),
    }
    repo(existing)
    # Try to give author 1 the email of author 2 -> should fail
    with pytest.raises(AuthorAlreadyExistsError):
        update_author_service(dummy_db, 1, email="b@mail.com")


# ───────────────────────────── Test: delete_author_service ──────────
def test_delete_author_success(dummy_db, repo):
    existing = {1: SimpleAuthor(1, "A", "a@mail.com")}
    dummy = repo(existing)

    delete_author_service(dummy_db, 1)
    assert 1 not in dummy.storage  # author removed


def test_delete_author_not_found(dummy_db, repo):
    repo()

    with pytest.raises(AuthorNotFoundError):
        delete_author_service(dummy_db, 42)
