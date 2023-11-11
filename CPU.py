

from tkinter import BooleanVar, Tk
from Memory import Memory
from Shared import SharedCPU, SharedClock, SharedMachine
from alu import ALU
from config import Config, GetConfig
from decoder import Decoder
from tk_manager import GetTK


class Clock(SharedClock):
    __tk    : Tk
    __cpu   : SharedCPU
    __cmp   : SharedMachine
    __dt    : int = 0

    def tick(self, step_fnc):
        step_fnc()
        self.__cpu.update_data_buffer()
        self.__cmp.update_addr_buffer()
        self.__tk.update()
        if self.wait.get(): return
        self.__tk.after(10, self.tick, step_fnc)

    def start(self, step_fnc):
        self.wait.set(False)
        self.tick(step_fnc)

    def stop(self):
        self.wait.set(True)

    def __init__(self, cpu:SharedCPU, cmp:SharedMachine) -> None:
        self.__tk = GetTK()
        self.__cmp = cmp
        self.__cpu = cpu
        self.__dt = GetConfig().clock_rate()

        super().__init__(self.__tk)
        
    
class CPU(SharedCPU):

    __clock : Clock

    alu     : ALU
    mem     : Memory

    __cnf   : Config

    def reset(self):
        self.inst_ptr = 0
        self.stck_ptr = self.__cnf.mem_size()
        
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

    def push_stack(self, val: int):
        self.stck_ptr -= 1
        self.mem.set_mem(self.stck_ptr, val)
        
    def pop_stack(self):
        v = self.mem.get(self.stck_ptr)
        self.stck_ptr += 1
        return v

    def start_clock(self, step_fnc):
        self.__clock.start(step_fnc)

    def stop_clock(self):
        self.__clock.stop()

    def get_clock(self):
        return self.__clock

    def __init__(self, cmp:SharedMachine, dec:Decoder) -> None:
        super().__init__()

        self.__cnf = GetConfig()

        self.reset()
        self.__clock = Clock(self, cmp)
        self.alu = ALU(dec, self, cmp)
        self.mem = cmp.get_mem()

