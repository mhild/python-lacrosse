from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from config import Config

#from testform import form

class PublicRouter(APIRouter):    

    def __init__(self):
        
        self.config = None      
        super().__init__()
    
    def set_config(self, _config:Config):
        self.config = _config
        self.config.loadConfig()
    
    def get_config(self):
        return self.config.config

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
    return templates.TemplateResponse(request=request, context = {'mappings' : router.get_config()}, name='dynamic/main.html')