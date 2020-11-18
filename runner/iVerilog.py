# iVerilog runner
from runner.Runner import Runner
from configs.config import Config
from utils.IO import IO
import os
import json
class iVerilog_Runner(Runner):
    config = Config.getConfig("configs/simulator/iverilog.json")

    def __init__(self, src, path):
        super().__init__(src, path)
        if "iVerilog-Path" in self.config:
            self.iv_path = self.config["iVerilog-Path"]
        else:
            self.iv_path = None
    
    def run(self, testcase, out):
        if self.iv_path == None:
            IO.writestr("! Runner(iverilog).run: iverilog not found.")
            return False
        r = super().run(testcase, out)
        if not r:
            return False
        src_unzip = self.path + "/src_unzip"
        # iverilog compile and run
        iverilog = (self.iv_path + os.sep if self.iv_path else "") + "iverilog"
        vvp = (self.iv_path + os.sep if self.iv_path else "") + "vvp"
        r = os.system("cd {1} && {0} -o mips.vvp tb.v mips.v".format(iverilog, src_unzip))
        if r != 0:
            IO.writestr("! Runner(iverilog).run: Error Occured on iVerilog Compiling")
            return False
        r = os.system("cd {path} && {vvp} src_unzip/mips.vvp > out/{out}".format(path=self.path, vvp=vvp, out=out))
        # r = os.system("cd {path} && {vvp} src_unzip/mips.vvp".format(path=self.path, vvp=vvp))
        if r != 0:
            IO.writestr("! Error Occured on iVerilog Running")
            return False
        return True
