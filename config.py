from threading import Lock
import os
import pickle
import json

DEVICE_DB_FILE=os.environ.get("JEELINK_DEVICE_DB_FILE", './jeelink_devices.pickle')


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
    
    def add_or_update(self, _id, _name=None):
        
        if _id not in self.config.keys():
            if _name is not None:
                raise UnknowmId()
            
            self.config[_id] = {}
        
        if _name is not None:
            for _item in self.config:
                if _item['name'] == _name:
                    raise NameNotUnique()

        
        self.config[_id]['name'] = _name