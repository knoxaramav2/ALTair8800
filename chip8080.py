from enum import Enum
from alu import ALU
import sys
from config import Config
import defs

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

      def deposit(self, byte):
          
          pass

      def clear(self):
          pass

      def __init__local__mem(self):
          for i in range(0, self.config.MemSize()):
              self.stack.append(0)

      def __init__(self):
        self.config = Config()
        self.__init__local__mem()
        

