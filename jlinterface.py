
import os
import pylacrosse
import codecs
import time
from icecream import ic

try:
    from ConfigParser import (ConfigParser, NoOptionError)
except ImportError:
    from configparser import (ConfigParser, NoOptionError)
    
JEELINK_DEVICE=os.environ.get("JEELINK_DEVICE", "/dev/ttyUSB0")
JEELINK_BAUD=os.environ.get("JEELINK_BAUD", 57600)



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
            
