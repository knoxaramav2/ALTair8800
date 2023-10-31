import numpy as np
from config import Config
from shared import SharedMemory

class Memory(SharedMemory):

    def get_stack(self, idx):
        return self.stack[idx]

    def set_stack(self, idx, val):
        self.stack[idx] = val

    def get_heap(self, idx):
        return self.heap[idx]

    # def heap_set(self, idx, val):
    #     self.heap[idx] = val

    def Reset(self):
        cfg = Config()
        self.stack = np.zeros(cfg.StackSize())
        self.heap = np.zeros(cfg.MemSize())

    def __init__(self) -> None:
        super().__init__()
        self.Reset()
        

__mem_inst__ : Memory = None

def GetMemory():
    global __mem_inst__
    if __mem_inst__ is None:
        __mem_inst__ = Memory()
    return __mem_inst__

