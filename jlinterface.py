
import os
import pylacrosse
import codecs
import time
from icecream import ic

from config import Config, NameNotUnique

try:
    from ConfigParser import (ConfigParser, NoOptionError)
except ImportError:
    from configparser import (ConfigParser, NoOptionError)
    
JEELINK_DEVICE=os.environ.get("JEELINK_DEVICE", "/dev/ttyUSB0")
JEELINK_BAUD=os.environ.get("JEELINK_BAUD", 57600)

class Jeelink():
    def __init__(self):
        self.jeelink = Jeelink_Worker()  
        self.config = Config()
        
        self.config.loadConfig() 
        
        
    def _update_known_sensors(self):
        _new_ids = self.jeelink.get_sensors().keys() - self.config.get_known_ids()
        
        for _id in _new_ids:
            self.config.add_or_update(_id)
        
    def get_sensor(self, id=None):
        self._update_known_sensors()
        return self.config.get_sensor(id)

    def set_sensor(self, id, name):
        self._update_known_sensors()
        
        self.config.add_or_update(id, name)
        
        
    def __str__(self):
        self._update_known_sensors()
        return str(self.config)   
            
            

class Jeelink_Worker():
    
    def get_sensors(self):
        return self.lacrosse.sensors

    def scan_callback(self, sensor, user_data):
        pass
        
    def scan(self, args, noblock=False):
        self.lacrosse.register_all(self.scan_callback, user_data=None)
        self.lacrosse.start_scan()
        
        if not noblock:
            while True:
                time.sleep(1)   

    def __del__(self):
        if self.lacrosse is not None:
            self.lacrosse.close()

    def __init__(self):

        self.lacrosse = None
        try:
            self.lacrosse = pylacrosse.LaCrosse(JEELINK_DEVICE, JEELINK_BAUD)
            self.lacrosse.open()
            
            self.scan(None, noblock=True)
            
            
            
        except:
            if self.lacrosse is not None:
                self.lacrosse.close()
            

    