

from chip8080 import Chip8080
from clock import Clock
from mem import Memory

 
class Machine:

    #components
    cpu : Chip8080
    mem : Memory
    clock : Clock

    def __init__(self) -> None:
        pass
