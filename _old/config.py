
import sys
from defs import MAX16, MAX8

class __config:

    __mem_size      = MAX16
    __stack_size    = MAX8

    __testMode      = False

    def IsDevMode(self):
        return self.__testMode

    def StackSize(self):
        return self.__stack_size

    def MemSize(self):
        return self.__mem_size
    
    def __parse_cmd(self, arg:str):
        terms = arg.split('=')
        k = terms[0]
        v = terms[1] if len(terms) == 2 else ''

        if k.startswith('--'):
            match k:
                case '--mem':
                    self.__mem_size = int(v)
                case _:
                    pass
        elif k[0] == '-' and v == '':
            match k:
                case '-d':
                    self.__testMode = True
        else:
            print('Invalid argument: ' + k +' ' + v)

    def __init__(self):
        for i,v in enumerate(sys.argv):
            if i == 0 : continue
            self.__parse_cmd(v)
        pass

__cnf_inst__ : __config = None

def Config():
    global __cnf_inst__
    if __cnf_inst__ is None:
        __cnf_inst__ = __config()
    return __cnf_inst__
