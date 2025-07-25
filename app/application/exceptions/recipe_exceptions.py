class RecipeNotFoundError(Exception):
    def __init__(self, recipe_id: int) -> None:
        super().__init__(f"Recipe with ID {recipe_id} not found.")

class RecipeAlreadyExistsError(Exception):
    def __init__(self, title: str):
        super().__init__(f"Recipe with the title: '{title}' already exists.")