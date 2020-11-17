'''
BUAA Computer Organization, Local Judger for Verilog
Judger Identifier: 19.06.C.O
*AUTHOR: dhy*
'''

from utils.Logger import Logger
from utils.IO import IO
from utils.Testcase import Testcase
from checker.Checker import Checker
from configs.config import Config
# Runners
from runner.iVerilog import iVerilog_Runner

# Judger
from judger.Judger import Judger

import os, sys

def main(args):
    if len(args) == 1:
        # TODO: launch GUI
        print("GUI Launch")
        pass
    else:
        # Parse Command Arguments
        argdict = {}
        for i in range(1, len(args)):
            if args[i] == '-run':
                if i == len(args) - 1:
                    print("! Error: no input task.")
                    return
                task = args[i + 1]
                if not os.path.exists(task):
                    print("! Error: task not exist")
                    return 
                argdict['run'] = task 
                continue
            if args[i] == '-load':
                if i == len(args) - 1:
                    print("! Error: No asm testcase input.")
                    return 
                testcase = args[i + 1]
                if not os.path.exists(testcase):
                    print("! Error: asm testcase not exist")
                    return 
                argdict['load'] = testcase
        if 'load' in argdict:
            Testcase.importAsm(argdict['load'],Config.getValue('configs/global.json', 'defaultTestcasePath'))
        if 'run' in argdict:
            jg = Judger(argdict['run'])
            jg.judge()
    pass 

if __name__ == '__main__':
    main(sys.argv)
