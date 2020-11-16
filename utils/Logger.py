# 日志记录
import json
import os
class Logger:
    @staticmethod
    def _logfilename():
        with open("configs/global.json", "r") as fp:
            config = json.loads(fp.read())
        
        if "logfile" in config:
            return config['logfile']
        return None
    logfile = _logfilename.__func__()
    @classmethod
    def writelog(cls, msg):
        if (cls.logfile == None):
            return
        if '/' in cls.logfile or '\\' in cls.logfile:
            path = os.path.dirname(cls.logfile)
            if not os.path.exists(path):
                os.mkdir(path)
        with open(cls.logfile, "a") as fout:
            fout.write(msg + "\n")
        pass