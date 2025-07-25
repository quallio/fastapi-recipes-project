from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from app.persistence.db import get_db
from app.application.security import decode_access_token
from app.persistence.repositories.user_repository import UserRepository
from app.domain.models.user import User

# Define the token URL for Swagger/OpenAPI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
user_repo = UserRepository()

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Dependency that returns the currently authenticated user.
    Raises 401 if token is invalid, expired, or user does not exist.
    """
    try:
        # Decode token and extract the 'sub' claim (email)
        email = decode_access_token(token)
    except JWTError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = user_repo.get_by_email(db, email)
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
