

from CPU import CPU
from Memory import Memory
from Shared import SharedMachine


class Machine(SharedMachine):

    cpu     : CPU
    mem     : Memory

    def __init__(self):
        self.cpu = CPU()
        self.mem = Memory()


        