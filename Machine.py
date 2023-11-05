

from CPU import CPU
from Memory import Memory
from Shared import SharedMachine
from tk_manager import GetTK


class Machine(SharedMachine):

    cpu     : CPU
    mem     : Memory

    def __init__(self):

        self.tk = GetTK()

        super().__init__(self.tk)

        self.cpu = CPU()
        self.mem = Memory()

        