

from Shared import ALU_Reg, SharedALU, SharedCPU, SharedCU, SharedMem
from decoder import Decoder


class ControlUnit(SharedCU):

     __cpu           : SharedCPU
     __alu           : SharedALU
     __mem           : SharedMem
     __dec           : Decoder
     __icc           : int
     __mar           : int = 0
     __mbr           : int = 0
     __ir            : int = 0

     __inst_len      : int = 1

     def __mov_pc_mar(self):
          self.__mar = self.__cpu.inst_ptr

     def __mov_mar_mbr(self):
               self.__mbr = self.__mem.get(self.__mar)
               self.__inst_len = self.__dec.inst_len(self.__mbr)
               if self.__inst_len >= 2:
                    self.__alu.set_reg(ALU_Reg.L, self.__mem.get(self.__mar+1))
               if self.__inst_len == 3:
                    self.__alu.set_reg(ALU_Reg.H, self.__mem.get(self.__mar+2))
          
     def __set_ir(self):
          self.__ir = self.__mbr          
          self.__cpu.next_addr(self.__inst_len)

     def step(self):
          #Fetch
          self.__mov_pc_mar()
          self.__mov_mar_mbr()
          self.__set_ir()

          #Execute
          self.__alu.execute(self.__ir)

          #Interrupt


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

     def __init__(self, scpu:SharedCPU, smem:SharedMem, sdec:Decoder) -> None:
          super().__init__()

          self.__cpu = scpu
          self.__alu = scpu.alu
          self.__mem = smem
          self.__dec = sdec
          self.__icc = 0
