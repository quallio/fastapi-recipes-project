from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.persistence.db import Base

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    # One-to-many relationship: an author can have many recipes
    # The cascade option ensures that when an Author is deleted,
    # all their associated recipes are also deleted
    recipes = relationship("Recipe", back_populates="author", cascade="all, delete-orphan")