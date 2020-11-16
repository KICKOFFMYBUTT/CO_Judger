# 图形界面与非图形界面的统一输出接口

class IO:
    redir = None # If NotNull,  To Window, Not Console
    @classmethod
    def writestr(cls, s):
        # default console
        if cls.redir == None:
            print(s)
