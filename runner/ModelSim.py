# Modelsim runner
from runner.Runner import Runner
from configs.config import Config
from utils.IO import IO
import os, shutil
import json

class ModelSim_Runner(Runner):
    config = Config.getConfig('configs/simulator/modelsim.json')

    def __init__(self, src, path):
        super().__init__(src, path)
        if 'modelsim-path' in self.config:
            self.sim_path = self.config['modelsim-path']
        else:
            self.sim_path = None
        if 'tcl' in self.config:
            self.tcl = self.config['tcl']
        else:
            self.tcl = None 
    
    def run(self, testcase, out):
        if self.sim_path == None:
            IO.writestr('! Runner(modelsim).run: ModelSim Simulator not configured.')
            return False
        if self.tcl == None:
            IO.writestr('! Runner(modelsim).run: Modelsim Tcl Batch not configured.')
            return False 
        r = super().run(testcase,out)
        if not r:
            return False
        # src_unzip = self.path + "/src_unzip"
        # copy the tcl batch
        # tcl_rawpath = 'configs/simulator/' + self.tcl_name
        # tcl = self.path + '/' + self.tcl_name
        # shutil.copyfile(src=tcl_rawpath, dst=tcl)
        tcl = "\n".join(self.tcl)
        tcl_name = 'run.do'
        with open(self.path + '/' + tcl_name, "w") as fp:
            fp.write(tcl)
        # modelsim compile and run
        vsim = (self.sim_path + '\\' if self.sim_path else '') + 'vsim.exe'
        cmd = 'cd {path} && \"{vsim}\" -c -do {tcl} > out/{out}'.format(
            path=self.path, vsim=vsim, tcl=tcl_name, out=out
        )
        # print(cmd)
        r = os.system(cmd)
        if r != 0:
            IO.writestr('! Error Occured on ModelSim Running')
            return False
        return True

    
    