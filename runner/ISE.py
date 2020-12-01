# ISE Runner
from runner.Runner import Runner
from configs.config import Config
from utils.IO import IO

import os, shutil, json
# "mips.exe -tclbatch ise.tcl > out\\{out}"
class ISE_Runner(Runner):
    config = Config.getConfig('configs/simulator/ise.json')

    def __init__(self, src, path):
        super().__init__(src, path)
        if 'ise-root' in self.config:
            self.ise_root = self.config['ise-root']
        else:
            self.ise_root = None
        self.ise_bin = str(self.ise_root) + '\\ISE\\bin\\nt64'
        if 'batch-compile' in self.config:
            self.batch_compile = self.config['batch-compile']
        else:
            self.batch_compile = None
        if 'batch-run' in self.config:
            self.batch_run = self.config['batch-run']
        else:
            self.batch_run = None
        if 'tcl' in self.config:
            self.tcl = self.config['tcl']
        else:
            self.tcl = None
    def compile(self):
        if self.ise_root == None:
            IO.writestr('! Runner(ise).compile: ISE Path not configured.')
            return False
        if self.batch_compile == None:
            IO.writestr('! Runner(ise).compile: Batch not configured.')
            return False
        src_list = " ".join(["src_unzip\\"+v for v in self.v_list])
        bat = "\r\n".join(self.batch_compile).format(
            root=self.ise_root, bin=self.ise_bin, path=self.path, src=src_list)
        bat = "@echo off\r\n" + bat
        with open(self.path + "\\compile.bat", "w") as fout:
            fout.write(bat)
        # Compile
        r = os.system("cd {path} && call compile.bat".format(path=self.path))
        if r != 0:
            IO.writestr('! Error Occured on ISE Compiling')
            return False
        return True
        
    def run(self, testcase, out):
        if self.batch_run == None:
            IO.writestr('! Runner(ise).run: Batch not configured.')
            return False
        if self.tcl == None:
            IO.writestr('! Runner(ise).run: Tcl not configured.')
            return False
        r = super().run(testcase, out)
        if not r:
            return False
        tcl = "\n".join(self.tcl)
        with open(self.path + '\\ise.tcl', "w") as fout:
            fout.write(tcl)
        # Run
        # r = os.system("{path}\\mips.exe -tclbatch {path}\\ise.tcl > {path}\\out\\{out}".format(path=self.path, out=out))
        bat = "\r\n".join(self.batch_run).format(
            root=self.ise_root, bin=self.ise_bin, path=self.path, out=out)
        bat = "@echo off\r\n" + bat
        with open(self.path + "\\run.bat", "w") as fout:
            fout.write(bat)
        # Compile
        r = os.system("cd {path} && call run.bat".format(path=self.path))
        if r != 0:
            IO.writestr('! Error Occured on ISE Running')
            return False
        return True
        