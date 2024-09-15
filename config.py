from threading import Lock
import os
import pickle
import json

from icecream import ic
from pylacrosse import LaCrosseSensor
from datetime import datetime
from dateutil import parser as dtparser
import pytz

DEVICE_DB_FILE=os.environ.get("JEELINK_DEVICE_DB_FILE", './jeelink_devices.pickle')
TIMEZONE=os.environ.get("TIMEZONE", 'Europe/Berlin')
MAX_AGE_IN_S=os.environ.get("MAX_AGE_IN_S", 10800)
class NameNotUnique(Exception):
    pass


class UnknownId(Exception):
    pass
class Config(object):
    
    def __init__(self):
        self.DB_LOCK = Lock()
        self.config = {}
        self.loadConfig()
    
    def get_sensor(self, id=None):
        if id is None:
            return self.config
        
        if id not in self.config.keys():
            return dict()
        
        return self.config[id]
    
    def get_sensor_name(self, id):
        _sensor = self.get_sensor(id)
        if 'name' in _sensor:
            return _sensor['name']
        
    def remove_orphaned_entries(self):
        
        now = datetime.now(tz=pytz.timezone(TIMEZONE))
        
        orphaned_sensors = []
        for id in self.config.keys():
            if 'lastseen' not in self.config[id] : continue
            lastseen = dtparser.parse(self.config[id]['lastseen'])
            if (now-lastseen).total_seconds() > MAX_AGE_IN_S:
                ic('removing orphaned sensor ', id)
                orphaned_sensors.append(id)
        
        ic(orphaned_sensors)
        
        if not orphaned_sensors:
            return
        
        for id in orphaned_sensors : del self.config[id]
        self.storeConfig()
            
    def update_state(self, sensor:LaCrosseSensor):
        self.remove_orphaned_entries()
        if sensor.sensorid not in self.config.keys():
            self.config[sensor.sensorid] = {}
        
        if sensor.sensorid in self.config.keys():
            #self.config[sensor.sensorid]['lastseen'] = datetime.now(tz=pytz.timezone(TIMEZONE))
            self.config[sensor.sensorid]['lastseen'] =f'{datetime.now(tz=pytz.timezone(TIMEZONE)):%Y-%m-%dT%H:%M:%S%z}'
            #YYYY-MM-DDTHH:mm:ss.sssZ
            self.config[sensor.sensorid]['battery_low'] = sensor.low_battery
            self.storeConfig()
        
        ic('update state')
        ic(self.config[sensor.sensorid])
        
        if 'name' in self.config[sensor.sensorid]:
            return self.config[sensor.sensorid]['name']
        else:
            return None
        
    
    def __str__(self):
        return json.dumps(self.config)
    
    
    def loadConfig(self):
        db = {}
        if os.path.isfile(DEVICE_DB_FILE):
            self.DB_LOCK.acquire()
            dbfile = open(DEVICE_DB_FILE, 'rb')    
            self.config = pickle.load(dbfile)
            dbfile.close()
            self.DB_LOCK.release()

    def storeConfig(self):
        self.DB_LOCK.acquire()
        dbfile = open(DEVICE_DB_FILE, 'wb+')
        pickle.dump(self.config, dbfile)                    
        dbfile.close()
        self.DB_LOCK.release()
        
    def get_known_ids(self):
        return self.config.keys()
    
    def delete(self, _id):
        ic('delete', _id) 
        del self.config[_id]
        self.storeConfig()
         
    def add_or_update(self, _id, _name=None):
        
        ic(self.config)
        if _id not in self.config.keys():
            if _name is not None:
                raise UnknownId()
            
            self.config[_id] = {}
        
        if _name is not None:
            for id in self.config.keys():
                if 'name' in self.config[id].keys():
                    if self.config[id]['name'] == _name:
                        raise NameNotUnique()

        
        self.config[_id]['name'] = _name
        self.config[_id]['lastseen'] =f'{datetime.now(tz=pytz.timezone(TIMEZONE)):%Y-%m-%dT%H:%M:%S%z}'

        self.storeConfig()