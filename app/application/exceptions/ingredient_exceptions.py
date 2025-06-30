class IngredientAlreadyExistsError(Exception):
    def __init__(self, name: str):
        super().__init__(f"Ingredient with name '{name}' already exists.")


class IngredientNotFoundError(Exception):
    def __init__(self, ingredient_id: int):
        super().__init__(f"Ingredient with ID {ingredient_id} not found.")


class IngredientInUseError(Exception):
    def __init__(self, ingredient_id: int):
        super().__init__(f"Ingredient with ID {ingredient_id} is used in a recipe and cannot be deleted.")
