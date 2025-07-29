from typing import List, Union

class IngredientAlreadyExistsError(Exception):
    def __init__(self, name: str):
        super().__init__(f"Ingredient with name '{name}' already exists.")

class IngredientNotFoundError(Exception):
    def __init__(self, missing_ids: Union[int, List[int]]):
        # Si viene un solo int, lo convertimos a lista
        if isinstance(missing_ids, int):
            missing_ids = [missing_ids]
        self.missing_ids = missing_ids

        # Formateamos el mensaje según cuántos IDs haya
        if len(missing_ids) == 1:
            msg = f"Ingredient with ID {missing_ids[0]} not found."
        else:
            msg = f"Ingredients with IDs {missing_ids} not found."
        super().__init__(msg)
class IngredientInUseError(Exception):
    def __init__(self, ingredient_id: int):
        super().__init__(f"Ingredient with ID {ingredient_id} is used in a recipe and cannot be deleted.")

class InvalidCSVError(Exception):
    def __init__(self, detail: str = "Only CSV files are supported"):
        super().__init__(detail)