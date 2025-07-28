from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.domain.schemas.user import UserCreate, UserOut, Token
from app.application.services.user_service import UserService
from app.application.services.user_service_provider import get_user_service
from app.application.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post(
    "/signup",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def signup(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service),
):
    """
    Create a new user account.
    Raises 400 if email is already registered.
    """
    try:
        return service.register(user_in)
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/token",
    response_model=Token,
    summary="Obtain a JWT access token",
)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service),
):
    """
    Authenticate user and return a JWT.
    Returns 401 if credentials are incorrect.
    """
    user = service.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}
