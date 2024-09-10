from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles


from routers import public
from routers import api

from jlinterface import Jeelink

app = FastAPI()

jeelink = Jeelink()

api.router.set_jeelink(jeelink)
public.router.set_jeelink(jeelink)

app.mount("/static", StaticFiles(directory="data/static"), name="static")

app.include_router(
    public.router,
    prefix=""
)

app.include_router(
    api.router,
    prefix="/api/v1"
)
