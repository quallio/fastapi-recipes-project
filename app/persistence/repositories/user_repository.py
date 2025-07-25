from sqlalchemy.orm import Session
from app.domain.models.user import User
from app.persistence.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, email: str) -> User | None:
        """
        Retrieve a user by email address.
        """
        return db.query(self.model).filter(self.model.email == email).first()

    def create(self, db: Session, *, email: str, hashed_password: str) -> User:
        """
        Create a new user with the given email and hashed password.
        """
        user = User(email=email, hashed_password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
