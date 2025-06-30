from fastapi import FastAPI
from app.presentation.routes import system

app = FastAPI(title="Recipes API", version="0.1.0")

app.include_router(system.router)



from fastapi import FastAPI

from app.presentation.routes import system
from app.presentation.routes import author_routes as author
from app.presentation.routes import recipe_routes as recipe
from app.presentation.routes import ingredients_routes as ingredient


app = FastAPI()

app.include_router(system.router)
app.include_router(author.router)
app.include_router(recipe.router)
app.include_router(ingredient.router)




