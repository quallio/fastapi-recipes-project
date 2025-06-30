from pydantic import BaseModel, EmailStr
from typing import Optional


# ─────────────────────────────── BASE ───────────────────────────────
class AuthorBase(BaseModel):
    name: str
    email: EmailStr


# ─────────────────────────────── CREATE ─────────────────────────────
class AuthorCreate(AuthorBase):
    pass


# ─────────────────────────────── UPDATE ─────────────────────────────
class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


# ─────────────────────────────── RESPONSE ───────────────────────────
class AuthorResponse(AuthorBase):
    id: int

    class Config:
        orm_mode = True
