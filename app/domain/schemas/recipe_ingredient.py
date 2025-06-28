from pydantic import BaseModel, condecimal, constr
from typing import Optional

# ─────────────────────────────────────────────────────────────
# Schemas for the many-to-many table recipe_ingredients
# ─────────────────────────────────────────────────────────────


class RecipeIngredientBase(BaseModel):
    """Fields common to both read & write representations."""
    quantity: condecimal(gt=0)          # > 0   (Decimal for precision if desired)
    unit: constr(strip_whitespace=True, min_length=1, max_length=10)


# -------- Input schema ---------------------------------------------------------
class RecipeIngredientCreate(RecipeIngredientBase):
    """
    Schema used when a client POSTs / PUTs a new ingredient into
    a recipe—expects only the foreign-keys plus the extra fields.
    """
    recipe_id: int
    ingredient_id: int


# -------- Output / read schema -------------------------------------------------
class RecipeIngredientRead(RecipeIngredientBase):
    """
    What the API returns when embedding ingredients inside a recipe
    (or if an endpoint lists the bridge table directly).
    """
    ingredient_id: int                 # keep IDs for reference
    ingredient_name: Optional[str] = None  # hydrated later in service layer

    class Config:
        orm_mode = True                # allow SQLAlchemy objects ⇒ Pydantic
