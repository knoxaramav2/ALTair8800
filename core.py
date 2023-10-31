from chip8080 import Chip8080
from mem import Memory
from shared import SharedMachine

class Machine(SharedMachine):

    #components
    cpu : Chip8080
    mem : Memory

    def toggle_power(self):
        self.power_on = not self.power_on

    def __init__(self) -> None:
        self.mem = Memory()
        self.cpu = Chip8080()
