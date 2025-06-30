class RecipeNotFoundError(Exception):
    def __init__(self, recipe_id: int) -> None:
        super().__init__(f"Recipe with ID {recipe_id} not found.")