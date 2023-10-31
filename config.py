
from defs import *

class Config:
    __mem_size__    = MAX16
    __stack_size__  = MAX8

__cnf_inst__ : Config = None

def GetConfig():
    global __cnf_inst__
    if __cnf_inst__ is None:
        __cnf_inst__ = Config()
    return __cnf_inst__

