# app/persistence/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from dotenv import load_dotenv
from typing import Generator
import os

# ───────────────────────────────────────
# Load .env and configure engine
# ───────────────────────────────────────
load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/recipes",
)

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

Base = declarative_base()

# ───────────────────────────────────────
# Dependency for FastAPI
# ───────────────────────────────────────
def get_db() -> Generator[Session, None, None]:
    """
    Yield a SQLAlchemy session per request and make sure it is closed.

    Usage in FastAPI:

        @router.get("/authors")
        def list_authors(db: Session = Depends(get_db)):
            ...
    """
    db: Session = SessionLocal()
    try:
        yield db          # the endpoint gets the session here
    finally:
        db.close()        # always executed, even on exceptions
