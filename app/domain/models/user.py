from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, Boolean, Enum as SQLEnum
from app.persistence.db import Base

class UserRole(str, PyEnum):
    user = "user"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email  = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(SQLEnum(UserRole), default=UserRole.user, nullable=False, index=True)
