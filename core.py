from chip8080 import Chip8080
from clock import Clock
from mem import Memory
from ui import UI

 
class Machine:

    #components
    ui : UI
    cpu : Chip8080
    mem : Memory
    clock : Clock

    def Start(self):
        self.ui.run()

    def __init__(self) -> None:

        self.clock = Clock()
        self.mem = Memory()
        self.cpu = Chip8080()
        self.ui = UI()
