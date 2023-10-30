import numpy as np
from config import Config
import defs

class Memory:

    stack = []
    heap  = []

    def Reset(self):
        cfg = Config()
        self.stack = np.empty(cfg.StackSize())
        self.heap = np.empty(cfg.MemSize())

    def __init__(self) -> None:
        self.Reset()
        

__mem_inst__ : Memory = None

def GetMemory():
    global __mem_inst__
    if __mem_inst__ is None:
        __mem_inst__ = Memory()
    return __mem_inst__

