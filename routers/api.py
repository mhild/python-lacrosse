from fastapi import APIRouter, Depends, Request, Response, HTTPException, Body

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from jlinterface import Jeelink_Worker

from typing import Dict, List, NamedTuple
from pydantic import BaseModel

from icecream import ic

from config import NameNotUnique, UnknownId
from jlinterface import Jeelink

import json
import os


class ItemNotFound(Exception):
    def __init__(self, id):
        self.id = id
        super().__init__()
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
        self.jeelink = None        
        super().__init__()
    
    def set_jeelink(self, _jeelink:Jeelink):
        self.jeelink = _jeelink
    
    def get_sensor(self, id=None):
        _sensors = self.jeelink.get_sensor(id)

        if id is not None and not _sensors:       
            raise ItemNotFound(id)
        
        return _sensors

    def delete_sensor(self, _id):
        self.jeelink.delete_sensor(_id)
        
    def set_sensor_mapping(self, id, name):
        
        ic("set_sensor_mapping", id, name)
        try:
            self.jeelink.set_sensor(id, name)
        except UnknownId:
            raise ItemNotFound(id)
        except NameNotUnique:
            raise DuplicateName()
        
        
router = SensorApiRouter()

#class NetLocations(BaseModel):
#    labels: set[str] = set()


class Ids(BaseModel):
    ids: list[int]  

class Mapping(BaseModel):
    id: int
    name: str


class Mappings(BaseModel):
    mappings: list[Mapping]
    
#@router.get("/sensors", response_model=NetLocations, tags=['data'])
@router.get("/sensors", tags=['data'])
async def get_sensors(request: Request):
    ic("### get sensors")
    # if net is None:
    #     raise HTTPException(status_code=400, detail="parameter net is missing")
    
    # if net not in locations.keys():
    #     raise HTTPException(status_code=404, detail="Item not found")
    
    result = router.get_sensor()
    ic(result)
    return JSONResponse(content=jsonable_encoder(result))

@router.put("/sensors", tags=['data'])
async  def set_sensors(mappings:Mappings, tags=["data"]):
    ic("### set sensors")

    try:
        for s in mappings.__dict__['mappings']:
            data = s.__dict__
            ic(data)
            router.set_sensor_mapping(data['id'], data['name'])
    except ItemNotFound as e:
        ic(e)
        raise HTTPException(status_code=404, detail=f"Item {e.id} not found")
    except DuplicateName as e:
        ic(e)
        raise HTTPException(status_code=400, detail="Name already taken")
    except Exception as e:
        ic(e)
        print(full_stack())
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return 'OK'
    

@router.delete("/sensors", tags=['data'])
async  def delete_sensors(ids:Ids, tags=["data"]):
    ic("### delete sensors")

    try:
        for id in ids.__dict__['ids']:
            router.delete_sensor(id)
    except ItemNotFound as e:
        ic(e)
        raise HTTPException(status_code=404, detail=f"Item {e.id} not found")
    except Exception as e:
        ic(e)
        print(full_stack())
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return 'OK'