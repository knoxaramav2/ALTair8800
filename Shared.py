from enum import Enum
import numpy as np
from tkinter import BooleanVar, Tk

from config import Config, GetConfig
from tk_manager import GetTK
from util import GetUtil, Util


class SharedMem:
    data            : [int] = []
    curr_data       : [BooleanVar] = []
    protect         : BooleanVar

    #Interface
    def set_curr_buffer(self, idx:int): pass
    def set_curr_data(self, idx:int, data:int):pass
    def reset(self): pass

    def get(self, idx:int) -> int:
        return self.data[idx]

    def __init__(self) -> None:
        cfg = GetConfig()
        tk = GetTK()
        self.protect = BooleanVar(tk, False)
        self.data = np.zeros(cfg.__mem_size__)
        for i in range(0, 8):
            self.curr_data.append(BooleanVar(tk, False))

ALU_Reg = Enum (
    'alu_reg',[
        'A', 'F',
        'B', 'C', 'BC',
        'D', 'E', 'DE',
        'H', 'L', 'HL'
    ]
)

class SharedALU:
    acc             : int = 0

    def get_reg(reg:ALU_Reg): pass
    def set_reg(reg:ALU_Reg, val:int): pass
    def get_acc(self):pass
    def set_acc(self, val:int):pass
    def get_flag_sign(self):pass
    def get_flag_zero(self):pass
    def get_flag_aux(self):pass
    def get_flag_parity(self):pass
    def get_flag_carry(self):pass
    def set_flags(self, sign:bool=None, zero:bool=None, aux:bool=None, parity:bool=None, carry:bool=None):pass

    def __init__(self) -> None:
        pass

class SharedCPU:
    inst_ptr        : int = 0
    mem_addr_reg    : int = 0
    mem_bffr_reg    : int = 0

    inte            : BooleanVar
    hlta            : BooleanVar
    wo              : BooleanVar
    wait            : BooleanVar
    memr            : BooleanVar
    int             : BooleanVar

    __mem           : SharedMem

    #Interface
    def reset(self):
        self.inte.set(False)
        self.hlta.set(False)
        self.wo.set(True)
        self.wait.set(True)
        self.memr.set(True)
        self.int.set(True)

    def next_addr(self, ln:int=1):
        self.inst_ptr += ln
        print('ADDR = %s'%self.inst_ptr)

    def jmp_addr(self, idx:int):
        self.inst_ptr += idx

    def set_word(self, data):
        self.__mem.set_curr_data(self.inst_ptr, data)
        print('SET %s at %s'%(self.__mem.get(self.inst_ptr), self.inst_ptr))

    def update_data_buffer(self) :
        self.__mem.set_curr_buffer(self.inst_ptr)

    def read_mem(self, offset:int=0):
        return self.__mem.data[self.inst_ptr+offset]

    def __init__(self, smem:SharedMem) -> None:
        tk = GetTK()
        
        self.__mem = smem
        self.inte = BooleanVar(tk, False)
        self.hlta = BooleanVar(tk, False)
        self.wo = BooleanVar(tk, True)
        self.wait = BooleanVar(tk, False)
        self.m1 = BooleanVar(tk, True)
        self.memr = BooleanVar(tk, True)
        self.int = BooleanVar(tk, False)
        
class SharedCU:

    M1          : BooleanVar
    wait        : BooleanVar

    #Interface
    def step(self): pass
    def set_MAR(self, addr: int): pass
    def get_MAR(self): pass
    def start_cycle(self): pass
    def halt(self): pass
    def start(self):pass
    def reset(self): pass

    def __init__(self) -> None:
        tk = GetTK()

        self.M1 = BooleanVar(tk, True)
        self.wait = BooleanVar(tk, True)

class SharedMachine:
    power_on        : BooleanVar
    run             : bool = False
    addr_sw         : [BooleanVar] = []
    addr_buffer     : [BooleanVar] = []
    data_buffer     : [BooleanVar] = []

    #Interface
    def get_sw_addr(self):pass
    def set_cpu_addr(self):pass
    def update_addr_buffer(self):pass
    def update_addr_pos(self):pass
    def reset(self):pass

    def reset_buffers(self, tk):
        for i in range(0, 16):
            self.addr_buffer[i].set(False)
        for i in range(0, 8):
            self.data_buffer[i].set(False)

    def __init__(self, tk:Tk) -> None:
        self.power_on = BooleanVar(tk, value=False)
        for i in range(0, 16):
            self.addr_sw.append(BooleanVar(tk, False))
            self.addr_buffer.append(BooleanVar(tk, False))
        for i in range(0, 8):
            self.data_buffer.append(BooleanVar(tk, False))
        

