from pydantic import BaseModel, EmailStr
from typing import Optional


class AuthorBase(BaseModel):
    name: str
    email: EmailStr


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class AuthorResponse(AuthorBase):
    id: int

    class Config:
        orm_mode = True
