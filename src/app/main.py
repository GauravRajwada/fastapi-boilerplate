from typing import Union

from fastapi import FastAPI
import os

# Env variables defined into docker-compose.yml
svc_name = os.getenv("APP_NAME", "FastAPI")

app_params = {
    "title": f"{svc_name} public API",
    "description": "{svc_name} public api",
    "version": "0.1.0",
    "docs_url": '/swagger',
    "redoc_url": '/docs',
}

app = FastAPI(**app_params)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# from app.views import user
from src.app.views import user

app.include_router(user.router)
