import os
import json
class Config:
    @staticmethod
    def getConfig(name: str):
        fname = name
        if not os.path.exists(fname):
            return None
        with open(fname, "r") as fp:
            raw = fp.read()
        return json.loads(raw)
    @staticmethod
    def saveConfig(name: str, conf: dict):
        fname = name
        dirname = os.path.dirname(fname)
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        with open(fname, "w") as fp:
            fp.write(json.dumps(conf))
        
    @staticmethod
    def getValue(confname: str, key: str):
        conf = Config.getConfig(confname)
        if conf is None:
            return None
        if key in conf:
            return conf[key]
        return None
    @staticmethod
    def setValue(confname: str, key: str, val):
        conf = Config.getConfig(confname)
        if conf is None:
            return 
        conf[key] = val
        fname = confname
        with open(fname, "w") as fp:
            fp.write(json.dumps(conf))
    