

from tkinter import Tk
from CPU import CPU
from Memory import Memory
from Shared import SharedMachine
from util import *
from tk_manager import GetTK


class Machine(SharedMachine):

    cpu     : CPU
    mem     : Memory

    __tk    : Tk
    __util  : Util

    def reset(self):
        self.reset_buffers(self.__tk)
        self.mem.reset()
        self.cpu.reset()

        print('RESET')
        print(self.cpu.inst_ptr)
        print(self.mem.get(0))

    def get_sw_addr(self):
        return self.__util.boolarr_to_int(self.addr_sw)

    def set_cpu_addr(self):
        if self.run: 
            print('BLOCKED')
            return

        self.cpu.mem_addr_reg = self.__util.boolarr_to_int(self.addr_sw)
        self.cpu.inst_ptr = self.cpu.mem_addr_reg
        self.__util.int_to_boolarr(self.cpu.mem_addr_reg, self.addr_buffer)
        self.cpu.update_data_buffer()
        self.mem.set_curr_buffer(self.cpu.inst_ptr)
    
    def update_addr_buffer(self):
        self.__util.int_to_boolarr(self.cpu.inst_ptr, self.addr_buffer)

    def update_addr_pos(self):
        pass

    def __init__(self):
        self.__tk = GetTK()
        self.__util = GetUtil()
        super().__init__(self.__tk)

        self.mem = Memory()
        self.cpu = CPU(self.mem)
        

        