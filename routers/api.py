from fastapi import APIRouter, Depends, Request, Response, HTTPException

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from jlinterface import Jeelink_Worker

from typing import Dict
from pydantic import BaseModel

from icecream import ic

from config import Config
import os


class ItemNotFound(Exception):
    pass
class DuplicateName(Exception):
    pass
class NoConstantsDefined(Exception):
    pass

def full_stack():
    import traceback, sys
    exc = sys.exc_info()[0]
    stack = traceback.extract_stack()[:-1]  # last one would be full_stack()
    if exc is not None:  # i.e. an exception is present
        del stack[-1]       # remove call of full_stack, the printed exception
                            # will contain the caught exception caller instead
    trc = 'Traceback (most recent call last):\n'
    stackstr = trc + ''.join(traceback.format_list(stack))
    if exc is not None:
         stackstr += '  ' + traceback.format_exc().lstrip(trc)
    return stackstr

class SensorApiRouter(APIRouter):    

    def __init__(self):
        
        self.config = None
        
        self.jeelink = Jeelink_Worker()        
        super().__init__()
    
    def set_config(self, _config:Config):
        self.config = _config
        self.config.loadConfig()
    
    def get_sensors(self, id=None, name=None):
        _raw = self.jeelink.get_sensors()
        _sensors = {}
        for _id in _raw.keys():
            _sensors[_id] = _raw[_id].__dict__
            _name = 'unknown'
            
            if _id in self.config.config.keys():
                _name = self.config.config[_id]['name']
    
            _sensors[_id]['name'] = _name
            
            if name is not None and name == _name:
                return _sensors[_id]
                
        if id is not None:
            if id in _sensors.keys():
                return _sensors['id']
            else:
                raise ItemNotFound()
            
        if name is not None:
            raise ItemNotFound()
        
        return _sensors

    def register_id(self, id, name):
        ic(f'register id {id}')
        if id not in self.config.config.keys():
            self.config.config[id] = {}
        ic("registering")
        self.config.config[id]['name'] = name
        ic("done")
        
    def set_sensor_mapping(self, id, name):
        
        ic("set_sensor_mapping")
        for _id in self.config.config.keys():
            if _id in self.config.config.keys():
                if self.config.config[_id]['name'] == name and id != _id:
                    raise DuplicateName()
        
        ic("update")
        ic(id)
        ic(router.get_sensors().keys())
        if id in router.get_sensors().keys():
            ic("id known")
            self.register_id(id, name)

            ic(self.config.config.keys())
            ic("store")
            self.config.storeConfig()
            
        else:
            raise ItemNotFound()
        
router = SensorApiRouter()

#class NetLocations(BaseModel):
#    labels: set[str] = set()

class SensorMapping(BaseModel):
    id: int
    name: str
    
#@router.get("/sensors", response_model=NetLocations, tags=['data'])
@router.get("/sensors", tags=['data'])
async def get_sensors(request: Request):
    ic("### get sensors")
    # if net is None:
    #     raise HTTPException(status_code=400, detail="parameter net is missing")
    
    # if net not in locations.keys():
    #     raise HTTPException(status_code=404, detail="Item not found")
    
    result = router.get_sensors()
    ic(result)
    return JSONResponse(content=jsonable_encoder(result))

@router.post("/sensors", tags=['data'])
async  def set_sensors(data:SensorMapping, tags=["data"]):
    ic("### set sensors")
    ic(data)
    
    try:
        router.set_sensor_mapping(data.id, data.name)
    except ItemNotFound as e:
        ic(e)
        raise HTTPException(status_code=404, detail="Item not found")
    except DuplicateName as e:
        ic(e)
        raise HTTPException(status_code=400, detail="Name already taken")
    except Exception as e:
        ic(e)
        print(full_stack())
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return 'OK'
    

