

from CPU import CPU
from Memory import Memory
from Shared import SharedMachine
from util import *
from tk_manager import GetTK


class Machine(SharedMachine):

    cpu     : CPU
    mem     : Memory

    __util  : Util

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
    
    def __init__(self):
        self.tk = GetTK()
        self.__util = GetUtil()

        super().__init__(self.tk)

        self.mem = Memory()
        self.cpu = CPU(self.mem)
        

        