from utils.IO import IO
from configs.config import Config
import os, shutil

class Testcase:

    def __init__(self):
        self.name = ""
        self.path = ""
        self.hex = ""
        self.asm = ""
        self.display = ""

    @staticmethod
    def loadFrom(confname):
        conf = Config.getConfig(confname)
        ret = Testcase()
        ret.path = os.path.dirname(confname)
        ret.name = conf['name']
        ret.hex = conf['hex']
        ret.asm = None
        ret.display = None
        if 'asm' in conf:
            ret.asm = conf['asm']
        if 'display' in conf:
            ret.display = conf['display']
        return ret
    @staticmethod
    def caseList():
        caselist = Config.getValue('configs/global.json', 'testcases')
        ret = []
        for item in caselist:
            # print(item)
            case = Testcase.loadFrom(item['path'])
            if not case is None:
                ret.append(case)
        return ret

    @staticmethod
    def importAsm(asm, dst):
        mars = Config.getValue('configs/global.json', 'marsPath')
        if os.path.exists(dst):
            shutil.rmtree(dst)
        os.mkdir(dst)
        testname = os.path.basename(asm).split('.')[0]
        # Create Test
        # asm
        asmname = testname + '.asm'
        shutil.copy(src=asm, dst=dst+'/'+testname+'/'+asmname)
        # hex
        hexname = testname + '.hex'
        os.system("java -jar {mars} nc mc CompactDataAtZero a dump .text HexText {hex} {asm}".format(
            mars=mars, hex=dst+'/'+testname+'/'+hexname, asm=dst+'/'+testname+'/'+asmname))
        # display
        dispname = testname + '.txt'
        os.system("java -jar {mars} nc mc CompactDataAtZero {asm} > {disp}".format(
            mars=mars, asm=dst+'/'+testname+'/'+asmname, disp=dst+'/'+testname+'/'+dispname))
        # json configuration
        jsonname = testname+'.json'
        caseconf = {"name": testname, "asm": asmname, "hex": hexname, "display": dispname}
        Config.saveConfig(dst+'/'+testname+'/'+jsonname, caseconf)
        # added into testcase-set
        testcases = Config.getValue('configs/global.json', 'testcases')
        testcases.append({'name': testname, 'path': dst+'/'+testname+'/'+jsonname})
    @staticmethod
    def rmcase(name):
        caselist = Config.getValue('configs/global.json', 'testcases')
        caselist.pop(name, 404)
        Config.setValue('configs/global.json', 'testcases', caselist)
    