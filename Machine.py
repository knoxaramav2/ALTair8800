

from tkinter import Tk
from CPU import CPU
from IOBufferLatch import IOBufferLatch
from Memory import Memory
from Shared import SharedMachine
from config import Config, GetConfig
from control_unit import ControlUnit
from decoder import Decoder
from devconn import DevConn
from util import *
from tk_manager import GetTK


class Machine(SharedMachine):

    __cpu     : CPU
    __mem     : Memory
    __cu      : ControlUnit
    __dec     : Decoder
    __io_latch: IOBufferLatch

    __tk    : Tk
    __util  : Util
    __cfg   : Config

    def reset(self):
        self.reset_buffers(self.__tk)
        self.__mem.reset()
        self.__cpu.reset()
        self.__cu.reset()
        print('RESET')

    def reset_addr_sw(self):
        self.__util.int_to_boolarr(0, self.addr_sw)

    def update_display(self):
        self.__tk.update()

    def get_sw_addr(self):
        return self.__util.boolarr_to_int(self.addr_sw)

    def set_cpu_addr(self):
        if self.run: 
            print('BLOCKED')
            return

        self.__cpu.mem_addr_reg = self.__util.boolarr_to_int(self.addr_sw)
        self.__cpu.inst_ptr = self.__cpu.mem_addr_reg
        self.__util.int_to_boolarr(self.__cpu.mem_addr_reg, self.addr_buffer)
        self.__cpu.update_data_buffer()
        self.__mem.set_curr_buffer(self.__cpu.inst_ptr)
    
    def update_addr_buffer(self):
        self.__util.int_to_boolarr(self.__cpu.inst_ptr, self.addr_buffer)

    def update_addr_pos(self):
        pass

    def get_cpu(self): return self.__cpu
    def get_mem(self): return self.__mem
    def get_cu(self): return self.__cu

    def __init__(self):
        self.__tk = GetTK()
        self.__util = GetUtil()
        self.__cfg = GetConfig()
        super().__init__(self.__tk)

        self.__mem = Memory()
        self.__dec = Decoder()
        self.io_latch = IOBufferLatch(self.__cfg.__dev_limit__)
        self.__cpu = CPU(self, self.__dec)
        self.__cu = ControlUnit(self.__cpu, self.__mem, self.__dec)
        

        