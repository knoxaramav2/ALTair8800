
import tkinter as tk
from tkinter import BooleanVar, IntVar, Tk


class SharedMem:
    data            : [int]
    curr_data       : int

class SharedCPU(SharedMem):
    inst_ptr        : int = 0
    mem_addr_reg    : int = 0
    mem_bffr_reg    : int = 0

    def next_addr(self):
        self.inst_ptr += 1

    def get_curr_dat(self) :
        self.curr_data = self.data[self.inst_ptr]
    
    def set_curr_dat(self, data) :
        self.data[self.inst_ptr] = data
        self.curr_data = data
        
class SharedMachine:
    power_on        : BooleanVar
    run             : bool = False
    addr_sw         : [BooleanVar] = []
    addr_buffer     : [BooleanVar] = []
    data_buffer     : [BooleanVar] = []

    #Interface
    def set_cpu_addr(self):pass

    def __init__(self, tk:Tk) -> None:
        self.power_on = BooleanVar(tk, value=False)
        for i in range(0, 16):
            self.addr_sw.append(BooleanVar(tk, False))
            self.addr_buffer.append(BooleanVar(tk, False))
        for i in range(0, 8):
            self.data_buffer.append(BooleanVar(tk, False))

