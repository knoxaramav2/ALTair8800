

from Shared import SharedALU, SharedCPU, SharedMem
from alu import ALU
from decoder import Decoder


class Clock:
    def __init__(self) -> None:
        pass
    
class CPU(SharedCPU):

    clock   : Clock
    alu     : ALU

    def reset(self):
        self.inst_ptr = 0
        
    def __init__(self, mem:SharedMem, dec:Decoder) -> None:
        super().__init__(mem)

        self.clock = Clock()
        self.alu = ALU(dec, self)

