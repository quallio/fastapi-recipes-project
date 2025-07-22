from fastapi import Request
from fastapi.responses import JSONResponse
from app.application.exceptions.author_exceptions import (
    AuthorAlreadyExistsError,
    AuthorNotFoundError,
)

def register_author_handlers(app):
    @app.exception_handler(AuthorAlreadyExistsError)
    async def author_already_exists_handler(request: Request, exc: AuthorAlreadyExistsError):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(AuthorNotFoundError)
    async def author_not_found_handler(request: Request, exc: AuthorNotFoundError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})
