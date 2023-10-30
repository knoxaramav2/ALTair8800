from enum import Enum
from alu import ALU
import sys
from config import Config
import defs
from mem import Memory

class Chip8080:
     
    #special registers
    mem_addr_ptr    : int   #16 bit
    mem_bffr_ptr    : int   #16 bit
    inst_ptr        : int   #16 bit
    stack_ptr       : int   #16 bit

    #working registers
    reg_b           : int   #8 bit
    reg_c           : int   #8 bit
    reg_d           : int   #8 bit
    reg_e           : int   #8 bit
    reg_h           : int   #8 bit
    reg_l           : int   #8 bit
    reg_acc         : int   #8 bit
    reg_stat        : int   #8 bit

    #components
    alu             : ALU
    mem             : Memory

    def deposit(self, byte):
        
        pass

    def clear(self):
        pass

    def __init__(self):
        self.config = Config()
        self.mem = Memory()

__chip_inst__ : Chip8080 = None

def GetChip8080():
    global __chip_inst__
    if __chip_inst__ is None:
        __chip_inst__ = Chip8080()
    return __chip_inst__
