from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from app.persistence.db import get_db
from app.application.security import decode_access_token
from app.persistence.repositories.user_repository import UserRepository
from app.domain.models.user import User, UserRole

# OAuth2 scheme for extracting the bearer token from requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Repository instance for user data access
user_repo = UserRepository()

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Dependency to retrieve the currently authenticated user.

    - Decodes and validates the JWT access token.
    - Fetches the corresponding user from the database.

    Raises:
        HTTPException 401 if the token is invalid, expired, or the user does not exist.

    Returns:
        User: The authenticated user instance.
    """
    try:
        # Decode JWT token and extract subject (email)
        email = decode_access_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Retrieve the user by email
    user = user_repo.get_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def get_current_active_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependency to verify that the current user has admin privileges.

    Raises:
        HTTPException 403 if the user does not have the 'admin' role.

    Returns:
        User: The authenticated user instance with admin role.
    """
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrators only",
        )
    return current_user
