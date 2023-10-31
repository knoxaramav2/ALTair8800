#User Device Exchange
import numpy as np
from core import Machine
# import chip8080 as lnkChip
# import core as lnkCore
# import ui as lnkUI
# import mem as lnkMem
#from chip8080 import Chip8080
#from core import GetMachine, Machine
#from ui import UI
#from mem import Memory

class UDX:

    comp : Machine = None
    chip = None
    mem = None

    data_state : list[int]
    addr_state : list[int]

    def UpdateUI(self):
        if self.comp.power_on == False:
            return    

        
        pass

    def update_data_info(self, data:int):
        for i in range(0, 8):
            self.data_state[i] = data & (1 << i)

    def update_addr_info(self, addr:int):
        for i in range(0, 15):
            self.data_state[i] = addr & (1 << i)

    def update_dat_addr_info(self, data:int, addr:int):
        self.update_data_info(data)
        self.update_addr_info(addr)

    def udx_examine_next(self):
        self.chip.ip_next()
        self.udx_examine()
        
    def udx_examine(self):
        self.update_dat_addr_info(
            self.mem.heap_get(self.chip.stack_ptr),
            self.chip.stack_ptr
        )

    def udx_deposit(self, data):
        self.data_state = data

    def udx_next_addr(self):
        self.chip.ip_next()

    def __init__(self):
        self.data_state = np.zeros(8)
        self.addr_state = np.zeros(16)

__udx_inst__ : UDX = None

def GetUDX():
    global __udx_inst__
    if __udx_inst__ is None:
        import core as lnkCore
        __udx_inst__ = UDX()
        __udx_inst__.comp = lnkCore.GetMachine()
        __udx_inst__.chip = __udx_inst__.comp.cpu
        __udx_inst__.mem = __udx_inst__.comp.mem
        
    return __udx_inst__