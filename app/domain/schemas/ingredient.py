from pydantic import BaseModel, Field, ConfigDict

# ─────────────────────── BASE ─────────────────────────
class IngredientBase(BaseModel):
    name: str = Field(..., example="Lemon Juice")


# ─────────────────────── CREATE ─────────────────────────
class IngredientCreate(IngredientBase):
    pass


# ─────────────────────── RESPONSE ─────────────────────────
class IngredientResponse(IngredientBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# ─────────────────────── IMPORT via CV  ─────────────────────────

class IngredientImportItem(BaseModel):
    name: str
    status: str
    id: int | None = None

    model_config = ConfigDict(from_attributes=True)