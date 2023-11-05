

from Shared import SharedCPU, SharedMem


class Clock:
    def __init__(self) -> None:
        pass

class ALU:
    def __init__(self) -> None:
        pass

class CPU(SharedCPU):

    clock   : Clock
    alu     : ALU

    def reset(self):
        self.inst_ptr = 0
        
    def __init__(self, mem:SharedMem) -> None:
        super().__init__(mem)

        self.clock = Clock()
        self.alu = ALU()

