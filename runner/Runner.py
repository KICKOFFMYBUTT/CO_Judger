'''
包含的要素：
1. 源代码的路径
2. 仿真软件的路径，所需的脚本等
3. 仿真软件的输出路径

要执行的事情：
1. 将源代码解压到指定的临时目录
2. 读取临时目录下的所有源代码
3. 编译, 调用仿真，保存输出
'''

import zipfile
import os, shutil
from utils.IO import IO
from configs.config import Config
from utils.Testcase import Testcase
class Runner:
    globconf = Config.getConfig("configs/global.json")
    def __init__(self, src, path):
        self.src = src
        self.path = path
        self.loadcode()
        pass

    def loadcode(self):
        if not os.path.exists(self.src): 
            IO.writestr("! Runner.loadcode: Source Not Exist!")
            return False
        src_unzip = self.path + '/' + 'src_unzip'
        self.src_unzip = src_unzip
        if os.path.exists(src_unzip):
            shutil.rmtree(src_unzip)
        os.mkdir(self.path + '/' + 'src_unzip')
        try:
            zip = zipfile.ZipFile(self.src)
            zip.extractall(src_unzip)
            zip.close()
        except:
            IO.writestr("! Runner.loadcode: Error occured on extracting zip")
            return False
        self.v_list = []
        for f in os.listdir(src_unzip):
            if f[:-2] == ".v":
                self.v_list.append(f)
                IO.writestr("# Extracted %s" % f)
        # copy testbench
        tb = self.globconf['testbench']
        shutil.copyfile(src=tb, dst=src_unzip+'/tb.v')
        return True

    def loadtest(self, testcase: Testcase):
        in_name = self.path + '/' + self.globconf['inputfilename']
        hexname = testcase.path + '/' + testcase.hex
        if not os.path.exists(hexname):
            IO.writestr('! Runner.loadtest: Hex Machine Code Not Exist')
            return False
        shutil.copyfile(src=hexname, dst=in_name)
        return True

    def run(self, testcase, out):
        r = self.loadtest(testcase)
        if not r:
            IO.writestr('! Runner.run: load testcase error.')
            return False
        ###### Code Here ######
        return True
