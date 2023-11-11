

from tkinter import BooleanVar, Tk
from Memory import Memory
from Shared import SharedCPU, SharedClock, SharedMachine
from alu import ALU
from decoder import Decoder
from tk_manager import GetTK


class Clock(SharedClock):
    __tk    : Tk

    def tick(self):
        self.__tk.update()

    def start(self):
        self.wait.set(False)

    def stop(self):
        self.wait.set(True)

    def __init__(self) -> None:
        self.__tk = GetTK()
        super().__init__(self.__tk)
        
    
class CPU(SharedCPU):

    __clock : Clock
    alu     : ALU
    mem     : Memory

    def reset(self):
        self.inst_ptr = 0
        
    def next_addr(self, ln:int=1):
        self.inst_ptr += ln

    def set_addr(self, addr):
        self.inst_ptr = addr

    def jmp_addr(self, idx:int):
        self.inst_ptr = idx

    def set_word(self, data, addr=None):
        if addr == None: addr = self.inst_ptr
        self.mem.set_mem(addr, data)

    def read_direct(self, offset: int):
        return self.read_mem(self.mar+offset, True)

    def update_data_buffer(self) :
        self.mem.set_curr_buffer(self.inst_ptr)

    def read_mem(self, offset:int=0, abs:bool=False):
        pos = self.inst_ptr+offset if not abs else offset
        return self.mem.data[pos]

    def start_clock(self):
        self.__clock.start()

    def stop_clock(self):
        self.__clock.stop()

    def get_clock(self):
        return self.__clock

    def __init__(self, cmp:SharedMachine, dec:Decoder) -> None:
        super().__init__()

        self.__clock = Clock()
        self.alu = ALU(dec, self, cmp)
        self.mem = cmp.get_mem()

