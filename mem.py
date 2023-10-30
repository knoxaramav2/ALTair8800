import numpy as np
from config import Config

class Memory:

    stack = []
    heap  = []

    def stack_get(self, idx):
        return self.stack[idx]

    def stack_set(self, idx, val):
        self.stack[idx] = val

    def heap_get(self, idx):
        return self.heap[idx]

    def heap_set(self, idx, val):
        self.heap[idx] = val

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

