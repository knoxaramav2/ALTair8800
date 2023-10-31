

from Shared import SharedCPU


class Clock:
    def __init__(self) -> None:
        pass

class ALU:
    def __init__(self) -> None:
        pass

class CPU(SharedCPU):

    clock   : Clock
    alu     : ALU

    def __init__(self) -> None:
        self.clock = Clock()
        self.alu = ALU()