from threading import Lock
import os
import pickle

DEVICE_DB_FILE=os.environ.get("JEELINK_DEVICE_DB_FILE", './jeelink_devices.pickle')

class Config(object):
    
    def __init__(self):
        self.DB_LOCK = Lock()
        self.config = {}
        self.loadConfig()
    
    
    
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