from pydantic import BaseModel

# ─────────────────────── BASE ─────────────────────────
class IngredientBase(BaseModel):
    name: str


# ─────────────────────── CREATE ─────────────────────────
class IngredientCreate(IngredientBase):
    pass


# ─────────────────────── RESPONSE ─────────────────────────
class IngredientResponse(IngredientBase):
    id: int

    class Config:
        orm_mode = True
