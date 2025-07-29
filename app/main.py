from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.presentation.exception_handlers import register_exception_handlers
from app.presentation.routes import system
from app.presentation.routes import author_routes as author
from app.presentation.routes import recipe_routes as recipe
from app.presentation.routes import ingredients_routes as ingredient
from app.presentation.routes import auth_routes as auth

# Create FastAPI app
app = FastAPI(title="Recipes API", version="0.1.0")

register_exception_handlers(app)

# Add CORS middleware for local development
origins = [
    "http://localhost:5173",     # Vite dev server
    "http://127.0.0.1:5173",     # Alternative localhost
    "http://localhost:8000",     # Swagger UI / FastAPI docs
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Use ["*"] only in non-sensitive dev environments
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routes
app.include_router(system.router)
app.include_router(author.router)
app.include_router(recipe.router)
app.include_router(ingredient.router)
app.include_router(auth.router)