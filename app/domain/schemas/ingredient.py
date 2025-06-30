from pydantic import BaseModel, Field

# ─────────────────────── BASE ─────────────────────────
class IngredientBase(BaseModel):
    name: str = Field(..., example="Lemon Juice")


# ─────────────────────── CREATE ─────────────────────────
class IngredientCreate(IngredientBase):
    pass


# ─────────────────────── RESPONSE ─────────────────────────
class IngredientResponse(IngredientBase):
    id: int

    class Config:
        orm_mode = True
