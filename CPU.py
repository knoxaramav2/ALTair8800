

from Memory import Memory
from Shared import SharedCPU, SharedMachine
from alu import ALU
from decoder import Decoder


class Clock:
    def __init__(self) -> None:
        pass
    
class CPU(SharedCPU):

    clock   : Clock
    alu     : ALU
    mem     : Memory

    def reset(self):
        self.inst_ptr = 0
        
    def next_addr(self, ln:int=1):
        self.inst_ptr += ln
        #print('ADDR = %s'%self.inst_ptr)

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


    def __init__(self, cmp:SharedMachine, dec:Decoder) -> None:
        super().__init__()

        self.clock = Clock()
        self.alu = ALU(dec, self, cmp)
        self.mem = cmp.get_mem()

