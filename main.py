'''
BUAA Computer Organization, Local Judger for Verilog
Judger Identifier: 19.06.C.O
*AUTHOR: dhy*
'''

from utils.Logger import Logger
from utils.IO import IO
from runner.iVerilog import iVerilog_Runner
from utils.Testcase import Testcase
from checker.Checker import Checker

from judger.Judger import Judger

# IO.writestr("hhhh")

# print(Testcase.caseList())
# cases = Testcase.caseList()
# for case in cases:
#     print(case.path, case.asm, case.hex, case.display)

# runner = iVerilog_Runner("E:\\programming\\BUAA_CO_2020\\P4_SingleCycleCPU\\pre\\src\\mips.zip", "demo/task1/")
# runner.run(cases[0], "out1.txt")

# r = Checker.check('demo/task1/out/out1.txt', 'testcase/weak1/test1.txt')
# # r = Checker.check('demo/task1/out/out1.txt', 'demo/task1/out/out1.txt')

# if r == None:
#     print("Checker Error")
# else :
#     print("Test Case #: {res}\nComment: {comment}".format(res=r[0],comment=r[1]))


jg = Judger('demo/task1/task1.json')
jg.judge()
print("-----------------------------")
jg = Judger('demo/task2/task2.json')
jg.judge()
