from app.persistence.db import engine, Base

# Import all models so they are registered in Base.metadata
import app.domain.models  # noqa: F401

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
