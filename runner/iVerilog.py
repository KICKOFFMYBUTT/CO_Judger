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
    
    def compile(self):
        if self.iv_path == None:
            IO.writestr("! Runner(iverilog).run: iverilog not found.")
            return False
        iverilog = (self.iv_path + os.sep if self.iv_path else "") + "iverilog"
        src_unzip = self.path + "/src_unzip"
        mips = " ".join(self.v_list)
        # print(self.v_list)
        r = os.system("cd {src} && {iverilog} -o mips.vvp tb.v {mips}".format(src=src_unzip, iverilog=iverilog,mips=mips))
        if r != 0:
            IO.writestr("! Runner(iverilog).run: Error Occured on iVerilog Compiling")
            return False
        return True

    def run(self, testcase, out):
        r = super().run(testcase, out)
        if not r:
            return False
        # iverilog run
        vvp = (self.iv_path + os.sep if self.iv_path else "") + "vvp"
        r = os.system("cd {path} && {vvp} src_unzip/mips.vvp > out/{out}".format(path=self.path, vvp=vvp, out=out))
        if r != 0:
            IO.writestr("! Error Occured on iVerilog Running")
            return False
        return True
