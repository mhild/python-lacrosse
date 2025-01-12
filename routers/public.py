from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from config import NameNotUnique, UnknownId
from jlinterface import Jeelink

from icecream import ic
#from testform import form

class PublicRouter(APIRouter):    

    def __init__(self):
        
        self.jeelink = None      
        super().__init__()
    
    def set_jeelink(self, _jeelink:Jeelink):
        self.jeelink = _jeelink
    
    def get_sensor(self):
        return self.jeelink.get_sensor()

router = PublicRouter()

templates = Jinja2Templates(directory="data/templates")


@router.get("/ping", tags=['administration'])
async def ping():
    return {"message": "Hello World"}

@router.get("/test", tags=['administration'])
async def test():
    return {"message": "Hello World"}

@router.get("/form", tags=['ui'])
async def webapp_form(request: Request):
    return templates.TemplateResponse(request=request, name='test.templ.html')

@router.get("/", tags=['ui'])
async def webapp_form(request: Request):
    #ic(router.get_sensor())
    return templates.TemplateResponse(request=request, context = {'mappings' : router.get_sensor()}, name='dynamic/main.html')