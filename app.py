from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles


from routers import public
from routers import api

from pylacrosse import LaCrosseSensor
from jlinterface import Jeelink
from config import Config

import mqtt
import json

from icecream import ic

### pyinstrument

# from pyinstrument import Profiler
# from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
# from starlette.requests import Request
# from starlette.responses import Response

# class PyInstrumentMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
#         profiler = Profiler(interval=0.001, async_mode="enabled")
#         profiler.start()
#         response = await call_next(request)
#         profiler.stop()
#         profiler.write_html("profile.html")
#         return response

###

app = FastAPI()
#app.add_middleware(PyInstrumentMiddleware)

config = Config()

def handle_jeelink_msg(sensor:LaCrosseSensor, user_data):
    #ic('got jeelink message')
    #ic(sensor.__dict__)
    id = sensor.__dict__['sensorid']
    #ic(config.get_sensor_name(id))
    #name = config.get_sensor_name(id)
    name = config.update_state(sensor)
    if name is not None:
        mqtt.send_message(name, json.dumps(sensor.__dict__))

jeelink = Jeelink(config, callback=handle_jeelink_msg)

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
