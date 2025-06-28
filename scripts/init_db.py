"""
Initialize the PostgreSQL schema by creating every table
registered in Base.metadata.

Run inside the running API container:

    docker-compose exec api python -m scripts.init_db
"""

import logging

from app.persistence.db import engine, Base

# Import all models so they are registered on Base.metadata
import app.domain.models  # noqa: F401  # pylint: disable=unused-import

# ───────────────────────────────────────────
# Configure basic logging to the console
# ───────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

def init_db() -> None:
    """
    Create all tables if they do not exist.
    Raises an exception if the operation fails.
    """
    logger.info("Starting database schema initialization...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database schema created (or already present)")
    except Exception as exc:
        logger.error("❌ Failed to initialize database schema: %s", exc)
        raise


if __name__ == "__main__":
    init_db()
