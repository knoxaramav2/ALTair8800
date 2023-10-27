
import sys
from defs import MAX16

class __config:

    __mem_size = MAX16

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
                    pass
                case _:
                    pass
        elif k[0] == '-' and v == '':
            pass
        else:
            print('Invalid argument: ' + k +' ' + v)

    def __init__(self):
        print('Init config')
        for i,v in enumerate(sys.argv):
            if i == 0 : continue
            self.__parse_cmd(v)
        pass

Config : __config

def Config():
    return __config()