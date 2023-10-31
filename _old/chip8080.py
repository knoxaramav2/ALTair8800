from alu import ALU
from clock import Clock
from shared import SharedChip, SharedMemory

class Chip8080(SharedChip):
    
    #special registers
    mem_addr_ptr    : int   #16 bit
    
    inst_reg        : int   #16 bit
    stack_ptr       : int   #16 bit

    #working registers
    reg_b           : int   #8 bit
    reg_c           : int   #8 bit
    reg_d           : int   #8 bit
    reg_e           : int   #8 bit
    reg_h           : int   #8 bit
    reg_l           : int   #8 bit
    reg_acc         : int   #8 bit
    reg_stat        : int   #8 bit

    #components
    alu             : ALU
    clock           : Clock
    mem             : SharedMemory

    def deposit(self, data):
        self.mem.heap_set(self.inst_ptr, data)

    def clear(self):
        self.mem_addr_ptr = 0
        self.mem_bffr_ptr = 0
        self.inst_ptr = 0
        self.inst_reg = 0
        self.stack_ptr = 0
        self.reg_b = 0
        self.reg_c = 0
        self.reg_d = 0
        self.reg_e = 0
        self.reg_h = 0
        self.reg_l = 0
        self.reg_acc = 0
        self.reg_stat = 0

    def ip_next(self):
        self.inst_ptr += 1

    def ip_set(self, addr:int):
        self.inst_ptr = addr

    def __init__(self):
        self.clear()

