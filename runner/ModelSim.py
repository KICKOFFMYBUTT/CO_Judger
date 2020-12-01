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
        if 'compile' in self.config:
            self.tcl_compile = self.config['compile']
        else:
            self.tcl_compile = None 
        if 'run' in self.config:
            self.tcl_run = self.config['run']
        else:
            self.tcl_run = None
    def compile(self):
        if self.sim_path == None:
            IO.writestr('! Runner(modelsim).run: ModelSim Simulator not configured.')
            return False
        if self.tcl_compile == None:
            IO.writestr('! Runner(modelsim).run: Modelsim Compile Tcl Batch not configured.')
            return False 
        
        tcl = "\n".join(self.tcl_compile)
        for v in self.v_list:
            tcl += '\nvlog src_unzip/{v}'.format(v=v)
        tcl_name = 'compile.do'
        with open(self.path + '/' + tcl_name, "w") as fp:
            fp.write(tcl)
        vsim = (self.sim_path + '\\' if self.sim_path else '') + 'vsim.exe'
        cmd = 'cd {path} && \"{vsim}\" -c -do {tcl} >nul 2>nul'.format(
            path=self.path, vsim=vsim, tcl=tcl_name
        )
        r = os.system(cmd)
        if r != 0:
            IO.writestr('! Error Occured on ModelSim Compileing')
            return False
        return True
    
    def run(self, testcase, out):
        r = super().run(testcase,out)
        if not r:
            return False
        tcl = "\n".join(self.tcl_run)
        tcl_name = 'run.do'
        with open(self.path + '/' + tcl_name, "w") as fp:
            fp.write(tcl)
        # modelsim compile and run
        vsim = (self.sim_path + '\\' if self.sim_path else '') + 'vsim.exe'
        cmd = 'cd {path} && \"{vsim}\" -c -do {tcl} > out/{out}'.format(
            path=self.path, vsim=vsim, tcl=tcl_name, out=out
        )
        r = os.system(cmd)
        if r != 0:
            IO.writestr('! Error Occured on ModelSim Running')
            return False
        return True

    
    