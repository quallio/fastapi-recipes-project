from fastapi import Request
from fastapi.responses import JSONResponse
from app.application.exceptions.ingredient_exceptions import (
    IngredientAlreadyExistsError,
    IngredientNotFoundError,
    IngredientInUseError,
    InvalidCSVError,
)

def register_ingredient_handlers(app):
    @app.exception_handler(IngredientAlreadyExistsError)
    async def ingredient_already_exists_handler(request: Request, exc: IngredientAlreadyExistsError):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(IngredientNotFoundError)
    async def ingredient_not_found_handler(request: Request, exc: IngredientNotFoundError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(IngredientInUseError)
    async def ingredient_in_use_handler(request: Request, exc: IngredientInUseError):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(InvalidCSVError)
    async def invalid_csv_exception_handler(request: Request, exc: InvalidCSVError):
        return JSONResponse(status_code=400, content={"detail": str(exc)})
    