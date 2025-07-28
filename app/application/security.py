# app/application/security.py

import time
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

# Create a Passlib context for Bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """
    Hash a plain-text password for storing in the database.
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against the stored hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str, expires_delta: Optional[int] = None) -> str:
    """
    Create a JWT token containing the given subject (e.g., user email or ID)
    and an expiration time.
    """
    # Calculate expiration timestamp (seconds since epoch)
    expire = int(time.time()) + (expires_delta or settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    to_encode = {"sub": subject, "exp": expire}
    # Encode JWT with HS256 algorithm
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> str:
    """
    Decode and validate a JWT token, returning the 'sub' claim (subject).
    Raises JWTError if token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError as e:
        # Re-raise so caller can convert to HTTPException(401)
        raise e
    subject: str = payload.get("sub")
    if subject is None:
        raise JWTError("Token missing subject claim")
    return subject
