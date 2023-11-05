import numpy as np
import tkinter as tk
from tkinter import BooleanVar, IntVar, Tk

from config import Config, GetConfig
from tk_manager import GetTK
from util import GetUtil, Util


class SharedMem:
    data            : [int] = []
    curr_data       : [BooleanVar] = []
    x : int
    #Interface
    def set_curr_buffer(self, idx:int): pass
    def set_curr_data(self, idx:int, data:int):pass
    def reset(self): pass

    def get(self, idx:int) -> int:
        return self.data[idx]

    def __init__(self) -> None:
        cfg = GetConfig()
        tk = GetTK()
        self.data = np.zeros(cfg.__mem_size__)
        for i in range(0, 8):
            self.curr_data.append(BooleanVar(tk, False))

class SharedCPU:
    inst_ptr        : int = 0
    mem_addr_reg    : int = 0
    mem_bffr_reg    : int = 0

    __util          : Util
    __mem           : SharedMem

    #Interface
    def reset(self):pass


    def next_addr(self):
        self.inst_ptr += 1

    def set_word(self, data):
        self.__mem.set_curr_data(self.inst_ptr, data)
        print('SET %s at %s'%(self.__mem.get(self.inst_ptr), self.inst_ptr))

    def update_data_buffer(self) :
        self.__mem.set_curr_buffer(self.inst_ptr)

    def get_curr_data(self):
        self.__util = GetUtil()
        return self.__mem.data[self.inst_ptr]

    def __init__(self, smem:SharedMem) -> None:
        self.__mem = smem
        
class SharedMachine:
    power_on        : BooleanVar
    run             : bool = False
    addr_sw         : [BooleanVar] = []
    addr_buffer     : [BooleanVar] = []
    data_buffer     : [BooleanVar] = []

    #Interface
    def get_sw_addr(self):pass
    def set_cpu_addr(self):pass
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
        

