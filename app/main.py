from fastapi import FastAPI
from app.presentation.routes import system

app = FastAPI(title="Recipes API", version="0.1.0")

app.include_router(system.router)
