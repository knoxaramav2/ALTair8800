
import tkinter as tk
from tkinter import BooleanVar, IntVar, Tk


class SharedMem:
    data            : [int]
    curr_data       : int

class SharedCPU(SharedMem):
    inst_ptr        : int
    mem_addr_reg    : int
    mem_bffr_reg    : int

    def get_curr_dat(self) :
        self.curr_data = self.data[self.inst_ptr]
    
    def set_curr_dat(self, data) :
        self.data[self.inst_ptr] = data
        self.curr_data = data
        
class SharedMachine:
    power_on        : BooleanVar

    def __init__(self, tk:Tk) -> None:
        self.power_on = BooleanVar(tk, value=False)
        
