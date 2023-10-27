from enum import Enum
from alu import ALU
import sys
from config import Config
import defs

#constants
class Instr:
    SKIP = 0x0

class StatBit:
    CARRY      = 0x1
    AUX_CARRY  = 0x2
    SIGN       = 0x4
    ZERO       = 0x8
    PARITY     = 0x10

#Component classes

class WRegs:
    
   L,H,E,D,C,B,F,A : int

   def __init__(self) -> None:
        pass

class Chip8080:
     
      #registers
      acc         : int    #8 bit
      flag        : int    #5 bit
      status      : int    #5 bit
      inst_reg    : int    
      prg_counter : int    #16 bit
      stck_ptr    : int    #16 bit

      #local memory
      stack = []

      #components
      alu   : ALU
      wr    : WRegs

      def __init__local__mem(self):
          for i in range(0, Config.MemSize()):
              self.stack.append(0)

      def __init__(self):
        

        self.__init__local__mem()
        

