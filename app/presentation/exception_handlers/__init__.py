from .author import register_author_handlers
from .ingredient import register_ingredient_handlers
from .recipe import register_recipe_handlers

def register_exception_handlers(app):
    register_author_handlers(app)
    register_ingredient_handlers(app)
    register_recipe_handlers(app)
