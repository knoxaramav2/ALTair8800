
import sys
from defs import *

class Config:

    __clock_rate__  = 2000000

    __dev_limit__   = 10
    __mem_size__    = MAX16
    __stack_size__  = MAX8

    __dbg_mode__    = False
    __dev0__        = False

    __prg_file__    = ''
    __alu_file__    = 'alu.cfg'

    def dev0(self): return self.__dev0__
    def mem_size(self): return self.__mem_size__
    def stack_size(self): return self.__stack_size__
    def debug_mode(self): return self.__dbg_mode__
    def program_file(self): return self.__prg_file__
    def clock_rate(self): return self.__clock_rate__
    def alu_profile(self): return self.__alu_file__

    def __parse_cmd(self, arg:str):
        terms = arg.split('=')
        k = terms[0]
        v = terms[1] if len(terms) == 2 else ''
        klen = len(k)

        if k.startswith('-') == False and k.startswith('--') == False:
            f'Invalid argument \'{k}\''
            return

        match k:
            case '-d': self.__dbg_mode__ = True

            case '--dev0': self.__dev0__ = True
            case '--devlim': self.__dev_limit__ = int(v)

            case '--memsize': self.__mem_size__=int(v)
            case '--stacksize': self.__stack_size__=int(v)

            case '--program': self.__prg_file__ = v
            case '--aludecode': self.__dec_file__ = v

            case '--clockrate': self.__clock_rate__ = int(v)

            case _: pass


    def __init__(self) -> None:
        for i,v in enumerate(sys.argv):
            if i == 0 : continue
            self.__parse_cmd(v)


__inst__ : Config = None

def GetConfig():
    global __inst__
    if __inst__ is None:
        __inst__ = Config()
    return __inst__

