# ISE Runner
from runner.Runner import Runner
from configs.config import Config
from utils.IO import IO

import os, shutil, json

class ISE_Runner(Runner):
    config = Config.getConfig('configs/simulator/ise.json')

    def __init__(self, src, path):
        super().__init__(src, path)
        if 'ise-root' in self.config:
            self.ise_root = self.config['ise-root']
        else:
            self.ise_root = None
        self.ise_bin = str(self.ise_root) + '\\ISE\\bin\\nt64'
        if 'batch' in self.config:
            self.batch = self.config['batch']
        else:
            self.batch = None
        if 'tcl' in self.config:
            self.tcl = self.config['tcl']
        else:
            self.tcl = None
    
    def run(self, testcase, out):
        if self.ise_root == None:
            IO.writestr('! Runner(ise).run: ISE Path not configured.')
            return False
        if self.batch == None:
            IO.writestr('! Runner(ise).run: Batch not configured.')
            return False
        if self.tcl == None:
            IO.writestr('! Runner(ise).run: Tcl not configured.')
            return False
        r = super().run(testcase, out)
        if not r:
            return False
        
        bat = "\r\n".join(self.batch).format(
            root=self.ise_root, bin=self.ise_bin, path=self.path, out=out)
        bat = "@echo off\r\n" + bat
        tcl = "\n".join(self.tcl)

        with open(self.path + "\\ise.bat", "w") as fout:
            fout.write(bat)
        with open(self.path + '\\ise.tcl', "w") as fout:
            fout.write(tcl)
        
        # Compile and run

        r = os.system("cd {path} && call ise.bat".format(path=self.path))
        if r != 0:
            IO.writestr('! Error Occured on ISE Running')
            return False
        return True
        