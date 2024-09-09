from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles

from config import Config

from routers import public
from routers import api

app = FastAPI()

config = Config()
api.router.set_config(config)
public.router.set_config(config)

app.mount("/static", StaticFiles(directory="data/static"), name="static")

app.include_router(
    public.router,
    prefix=""
)

app.include_router(
    api.router,
    prefix="/api/v1"
)
