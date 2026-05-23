# FastAPI application entry point
from fastapi import FastAPI

from .api.router import router as api_router

app = FastAPI(title="Game Asset Generator", version="0.1.0")
app.include_router(api_router)
