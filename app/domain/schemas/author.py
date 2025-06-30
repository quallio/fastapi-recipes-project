from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# ─────────────────────────────── BASE ───────────────────────────────
class AuthorBase(BaseModel):
    name: str = Field(..., example="Pepe Argento")
    email: EmailStr = Field(..., example="pepe_argg@mail.com")


# ─────────────────────────────── CREATE ─────────────────────────────
class AuthorCreate(AuthorBase):
    pass


# ─────────────────────────────── UPDATE ─────────────────────────────
class AuthorUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Franco Colap")
    email: Optional[EmailStr] = Field(None, example="franco_c@mail.com")


# ─────────────────────────────── RESPONSE ───────────────────────────
class AuthorResponse(AuthorBase):
    id: int

    class Config:
        orm_mode = True
