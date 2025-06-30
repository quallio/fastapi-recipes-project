from pydantic import BaseModel

class IngredientBase(BaseModel):
    name: str


class IngredientCreate(IngredientBase):
    pass


class IngredientRead(IngredientBase):
    id: int

    class Config:
        orm_mode = True

# working on...
