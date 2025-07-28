from typing import Optional
from sqlalchemy.orm import Session

from app.domain.models.user import User
from app.domain.schemas.user import UserCreate
from app.application.security import hash_password, verify_password
from app.persistence.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository()

    def register(self, user_in: UserCreate) -> User:
        """
        Register a new user.
        Raises ValueError if email is already taken.
        """
        if self.repo.get_by_email(self.db, user_in.email):
            raise ValueError("Email already registered")
        hashed = hash_password(user_in.password)
        return self.repo.create(self.db, email=user_in.email, hashed_password=hashed)

    def authenticate(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate user credentials.
        Returns the User if valid, else None.
        """
        user = self.repo.get_by_email(self.db, email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
