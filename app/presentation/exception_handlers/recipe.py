from fastapi import Request
from fastapi.responses import JSONResponse
from app.application.exceptions.recipe_exceptions import RecipeNotFoundError

def register_recipe_handlers(app):
    @app.exception_handler(RecipeNotFoundError)
    async def recipe_not_found_handler(request: Request, exc: RecipeNotFoundError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})
