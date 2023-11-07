

from Shared import SharedCPU, SharedCU, SharedMem
from decoder import Decoder


class ControlUnit(SharedCU):

    __cpu       : SharedCPU
    __mem       : SharedMem
    __dec       : Decoder
    __icc       : int
    __mar       : int = 0
    __mbr       : int = 0
    __ir        : int = 0

    def __mov_pc_mar(self):
         self.__mar = self.__cpu.inst_ptr

    def __mov_mar_mbr(self):
         self.__mbr = self.__mem.get(self.__mar)
         inst_len = self.__dec.inst_len(self.__mbr)
         if inst_len >= 1:
              pass
         if inst_len == 2:
              pass
         self.__cpu.next_addr(inst_len)

    def __mov_mbr_ir(self):
         self.__ir = self.__mbr

    def step(self):
        match self.__icc:
            case 0: #Fetch
                self.__mov_pc_mar()
                self.__mov_mar_mbr()
                self.__mov_mbr_ir()
            case 1:#Ind. Acc
                pass
            case 2:#Exec
                pass
            case 3:#Interrupt
                self.__icc = 0


    def set_MAR(self, addr: int):
         self.__mar = addr
    
    def get_MAR(self):
         return self.__mar
    
    def start_cycle(self):
         self.M1.set(True)
         self.wait.set(False)

    def halt(self):
         self.wait.set(True)

    def start(self):
         self.wait.set(False)

    def reset(self):
         self.halt()
         self.__icc = 0
         self.M1.set(True)

    def __init__(self, scpu:SharedCPU, smem:SharedMem, dec:Decoder) -> None:
        super().__init__()

        self.__cpu = scpu
        self.__mem = smem
        self.__dec = dec
        self.__icc = 0
