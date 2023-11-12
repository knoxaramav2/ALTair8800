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
    def set_mem(self, idx:int, data:int):pass
    def reset(self): pass

    def get(self, idx:int) -> int:
        return self.data[idx]

    def __init__(self) -> None:
        cfg = GetConfig()
        tk = GetTK()
        self.protect = BooleanVar(tk, False)
        self.data = [0] * cfg.__mem_size__
        for i in range(0, 8):
            self.curr_data.append(BooleanVar(tk, False))

ALU_Reg = Enum (
    'alu_reg',[
        #3 bit
        'B', 'C',
        'D', 'E',
        'H', 'L',
        'M', 'A',
        #2 bit
        'BC', 'DE', 'HL', 'MA'
    ]
)

ALU_Flag = Enum (
    'alu_flag',[
        'C', 'P', 'A', 'Z', 'S' 
    ]
)

class SharedALU:
    def execute(self, inst:int):pass
    def read_reg(self, reg:ALU_Reg):pass
    def set_reg(self, reg:ALU_Reg, val:int):pass
    def read_flag(self, flag:ALU_Flag):pass
    def set_flag(self, flag:ALU_Flag, val:int):pass

    def set_cu(self, cu):pass#TODO Less hacky solution

    def __init__(self) -> None:
        pass

class SharedCPU:
    inst_ptr        : int = 0
    stck_ptr        : int = 0
    mem_addr_reg    : int = 0
    mem_bffr_reg    : int = 0

    inte            : BooleanVar
    hlta            : BooleanVar
    wo              : BooleanVar
    wait            : BooleanVar
    memr            : BooleanVar
    intt            : BooleanVar

    mar             : int = 0
    mbr             : int = 0
    ir              : int = 0

    #Interface
    def reset(self): pass
    def next_addr(self, ln:int=1): pass
    def set_addr(self, addr): pass
    def jmp_addr(self, idx:int): pass
    def read_direct(self, offset:int): pass
    def write_direct(self, offset:int): pass
    def set_word(self, data, addr=None): pass
    def update_data_buffer(self) :  pass

    def get_instr(self): pass
    def get_mar(self): pass
    def get_mbr(self): pass

    def push_stack(self, val:int):pass
    def pop_stack(self):pass

    def start_clock(self, step_func): pass
    def stop_clock(self): pass
    def get_clock(self): pass

    def __init__(self) -> None:
        tk = GetTK()
        
        self.inte = BooleanVar(tk, False)
        self.hlta = BooleanVar(tk, False)
        self.wo = BooleanVar(tk, True)
        self.wait = BooleanVar(tk, False)
        self.m1 = BooleanVar(tk, True)
        self.memr = BooleanVar(tk, True)
        self.intt = BooleanVar(tk, False)
        
class SharedClock:

    wait    : BooleanVar

    def __init__(self, tk:Tk) -> None:
        self.wait = BooleanVar(tk, True)

class SharedCU:

    M1          : BooleanVar
    wait        : BooleanVar
    sclock      : SharedClock

    #Interface
    def step(self): pass
    def set_MAR(self, addr: int): pass
    def get_MAR(self): pass
    def start_cycle(self): pass
    def halt(self): pass
    def start(self):pass
    def reset(self): pass
    def read_mem(self, idx): pass

    def __init__(self, clk:SharedClock) -> None:
        tk = GetTK()
        self.sclock = clk
        self.M1 = BooleanVar(tk, True)
        self.wait = self.sclock.wait

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
    def reset_addr_sw(self):pass
    def update_display(self):pass

    def get_cpu(self) -> SharedCPU: pass
    def get_mem(self) -> SharedMem: pass
    def get_cu(self) -> SharedCU: pass

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
        

