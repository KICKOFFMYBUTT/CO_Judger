# Display Checker
from utils.IO import IO
import os, shutil
class Checker:
    @staticmethod
    def timetrim(src, dst):
        if not os.path.exists(src):
            IO.writestr("! timetrim: {src} not found.".format(src=src))
            return False
        if not os.path.exists(os.path.dirname(dst)):
            os.mkdir(os.path.dirname(dst))
        cmd = "checker\\timeprocess.exe < {0} > {1}".format(src, dst)
        r = os.system(cmd)
        if r != 0:
            IO.writestr("! timetrim: error running timeprocess.exe")
            return None
        
    @staticmethod
    def check(src1, src2):
        if not os.path.exists(src1):
            IO.writestr("! checker: {src} not found".format(src=src1))
            return None
        if not os.path.exists(src2):
            IO.writestr("! checker: {src} not found".format(src=src2))
            return None
        cmd = "checker\\displaychecker.exe {0} {1}".format(src1, src2)
        # print("> {cmd}".format(cmd=cmd))
        res = os.popen(cmd)
        res_lines = res.readlines()
        res_lines = [line.strip() for line in res_lines]
        valid_lines = []
        for l in res_lines:
            if len(l) != 0 and l[0] != '-':
                valid_lines.append(l)
            # print(l)
        res_lines = valid_lines
        # print(res_lines)
        if res_lines[-1].strip() == 'Accepted' :
            return ('Accepted', 'Accepted')
        elif res_lines[-1].strip() == 'Wrong Answer' :
            return ('Wrong Answer', "\n".join(res_lines[0:-1]))
        else:
            return None
