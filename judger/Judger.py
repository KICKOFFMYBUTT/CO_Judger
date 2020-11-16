'''
评测机基本功能：
根据 task 去初始化，选取仿真工具，加载测试数据集。


'''
from configs.config import Config
from checker.Checker import Checker
from utils.Testcase import Testcase
from utils.IO import IO

import runner

import os, shutil
class Judger:
    def loadTestSet(self):
        globalTestcases = Config.getValue('configs/global.json', 'testcases')
        self.testcaseSet = []
        for test in self.task['testcases']:
            for stdtest in globalTestcases:
                if test['name'] == stdtest['name']:
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
            self.runner_type = runner.iVerilog.iVerilog_Runner
        elif self.task['tool'] == 'ise':
            pass
        elif self.task['tool'] == 'modelsim':
            pass
        else:
            self.runner_type = None
        # load testcases
        self.loadTestSet()
    
    def patmode(self):

        pass
    def stdmode(self):
        IO.writestr('Judger Identifier: {id}'.format(id=Config.getValue('configs/global.json', 'identifier')))
        IO.writestr(' - Standard Mode - ')
        runner = self.runner_type(self.task['src'], self.path)
        for test in self.testcaseSet:
            runner.run(test, 'out.txt')
            res = Checker.check(test.path + '/' + test.display, self.path + '/out/out.txt')
            outstr = 'Test Case #<{name}>: '.format(name=test.name)
            if res == None:
                outstr += 'Checker Error'
            else :
                outstr += "{res} \nComment: {comment}".format(res=res[0],comment=res[1])
            IO.writestr(outstr)
            
        pass 

    def judge(self):
        if self.mode == 'standard':
            return self.stdmode()
        elif self.mode == 'pat':
            return self.patmode()
        else:
            IO.writestr('! Judger: invalid mode')
            return False



    
