from fastapi import FastAPI
from app.presentation.routes import system

app = FastAPI(title="Recipes API", version="0.1.0")

app.include_router(system.router)



from fastapi import FastAPI

from app.presentation.routes import system
from app.presentation.routes import author_routes as author

app = FastAPI()

app.include_router(system.router)
app.include_router(author.router)
