'''
评测机基本功能：
根据 task 去初始化，选取仿真工具，加载测试数据集。


'''
from configs.config import Config
from checker.Checker import Checker
from utils.Testcase import Testcase
from utils.IO import IO

from runner import iVerilog, ModelSim, ISE

import os, shutil
class Judger:
    def loadTestSet(self):
        globalTestcases = Config.getValue('configs/testcase.json', 'testcases')
        self.testcaseSet = []
        for test in self.task['testcases']:
            for stdtest in globalTestcases:
                if test == stdtest['name']:
                    self.testcaseSet.append(Testcase.loadFrom(stdtest['path']))
                    break
    def __init__(self, task):
        self.task = Config.getConfig(task)
        self.path = os.path.dirname(task)
        # mode
        self.mode = self.task['mode']
        # load tool runner
        self.runner_type = None
        if self.task['tool'] == 'iverilog':
            self.runner_type = iVerilog.iVerilog_Runner
        elif self.task['tool'] == 'ise':
            self.runner_type = ISE.ISE_Runner
        elif self.task['tool'] == 'modelsim':
            self.runner_type = ModelSim.ModelSim_Runner
        else:
            self.runner_type = None
        # load testcases
        self.loadTestSet()
    
    def patmode(self):
        IO.writestr('Judger Identifier: {id}'.format(id=Config.getValue('configs/global.json', 'identifier')))
        IO.writestr('Simulation Tool: {sim}'.format(sim=self.task['tool']))
        IO.writestr(' - Pat Mode - ')
        runner1 = self.runner_type(self.task['src1'], self.path)
        r = runner1.compile()
        if not r:
            IO.writestr('src1 Compile Error')
            return
        runner2 = self.runner_type(self.task['src2'], self.path)
        r = runner2.compile()
        if not r:
            IO.writestr('src2 Compile Error')
            return
        for test in self.testcaseSet:
            outstr = 'Test Case #<{name}>: '.format(name=test.name)
            r = runner1.run(test, 'out1.txt')
            if not r:
                outstr += "{res} \nComment: {comment}".format(res='Runtime Error',comment='src1 Runtime Error')
            r = runner2.run(test, 'out2.txt')
            if not r:
                outstr += "{res} \nComment: {comment}".format(res='Runtime Error',comment='src2 Runtime Error')
            Checker.timetrim(self.path + '/out/out1.txt', self.path + '/out/out1_t.txt')
            Checker.timetrim(self.path + '/out/out2.txt', self.path + '/out/out2_t.txt')
            res = Checker.check(self.path + '/out/out1_t.txt', self.path + '/out/out2_t.txt')
            if res == None:
                outstr += 'Checker Error'
            else :
                outstr += "{res} \nComment: {comment}".format(res=res[0],comment=res[1])
            IO.writestr(outstr)
    def stdmode(self):
        IO.writestr('Judger Identifier: {id}'.format(id=Config.getValue('configs/global.json', 'identifier')))
        IO.writestr('Simulation Tool: {sim}'.format(sim=self.task['tool']))
        IO.writestr(' - Standard Mode - ')
        runner = self.runner_type(self.task['src'], self.path)
        r = runner.compile()
        if not r:
            IO.writestr('Compile Error')
            return
        for test in self.testcaseSet:
            if not test.display:
                IO.writestr('# Test Case #<{name}>: Omitted\nComment: Standard Answer not ready.'.format(name=test.name))
                continue
            outstr = 'Test Case #<{name}>: '.format(name=test.name)
            r = runner.run(test, 'out.txt')
            if not r:
                outstr += "{res} \nComment: {comment}".format(res='Runtime Error', comment='Runtime Error')
                IO.writestr(outstr)
                break
            Checker.timetrim(test.path + '/' + test.display, self.path + '/out/std_t.txt')
            Checker.timetrim(self.path + '/out/out.txt', self.path + '/out/out_t.txt')
            # res = Checker.check(test.path + '/' + test.display, self.path + '/out/out.txt')
            res = Checker.check(self.path + '/out/std_t.txt', self.path + '/out/out_t.txt')
            outstr = 'Test Case #<{name}>: '.format(name=test.name)
            if res == None:
                outstr += 'Checker Error'
            else :
                outstr += "{res} \nComment: {comment}".format(res=res[0],comment=res[1])
            IO.writestr(outstr) 

    def judge(self):
        # check runner
        if self.runner_type == None:
            IO.writestr('! Judger: not supported simulation tool')
        if self.mode == 'standard':
            return self.stdmode()
        elif self.mode == 'pat':
            return self.patmode()
        else:
            IO.writestr('! Judger: invalid mode')
            return False



    
