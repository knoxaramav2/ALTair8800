

from Shared import SharedALU, SharedCPU, SharedCU, SharedMem
from decoder import Decoder


class ControlUnit(SharedCU):

     __cpu           : SharedCPU
     __alu           : SharedALU
     __mem           : SharedMem
     __dec           : Decoder

     __inst_len      : int = 1

     def __mov_pc_mar(self):
          self.__cpu.mar = self.__cpu.inst_ptr

     def __mov_mar_mbr(self):
          self.__cpu.mbr = self.__mem.get(self.__cpu.mar)
          self.__inst_len = self.__dec.inst_len(self.__cpu.mbr)+1
          
     def __set_ir(self):
          self.__cpu.ir = self.__cpu.mbr          
          self.__cpu.next_addr(self.__inst_len)

     def step(self):
          #Fetch
          self.__mov_pc_mar()
          self.__mov_mar_mbr()
          self.__set_ir()
          
          #Execute
          self.__alu.execute(self.__cpu.ir)

          #Interrupt

     def set_MAR(self, addr: int):
          self.__cpu.mar = addr
     
     def get_MAR(self):
          return self.__cpu.mar
     
     def start_cycle(self):
          self.M1.set(True)
          self.wait.set(False)

     def halt(self):
          self.wait.set(True)

     def start(self):
          self.wait.set(False)
          self.__cpu.start_clock(lambda:self.step())

     def reset(self):
          self.halt()
          self.__icc = 0
          self.M1.set(True)

     def read_mem(self, idx):
          return self.__mem.get(idx)

     def __init__(self, scpu:SharedCPU, smem:SharedMem, sdec:Decoder) -> None:
          self.__cpu = scpu
          self.__alu = scpu.alu
          self.__alu.set_cu(self)
          self.__mem = smem
          self.__dec = sdec
          
          super().__init__(self.__cpu.get_clock())

          