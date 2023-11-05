

from CPU import CPU
from Memory import Memory
from Shared import SharedMachine
from util import *
from tk_manager import GetTK


class Machine(SharedMachine):

    cpu     : CPU
    mem     : Memory

    __util  : Util

    def set_cpu_addr(self):
        self.cpu.mem_addr_reg = self.__util.boolarr_to_int(self.addr_sw)
        self.__util.int_to_boolarr(self.cpu.mem_addr_reg, self.addr_buffer)
        self.__util.int_to_boolarr(self.cpu.get_curr_dat(), self.data_buffer)
    def __init__(self):

        self.tk = GetTK()
        self.__util = GetUtil()

        super().__init__(self.tk)

        self.cpu = CPU()
        self.mem = Memory()

        