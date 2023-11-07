

from enum import Enum
from Shared import ALU_Reg, SharedALU, SharedCPU, SharedCU, SharedMem
from decoder import Decoder


class Clock:
    def __init__(self) -> None:
        pass

class ALU(SharedALU):

    __dec       : Decoder
    __reg_AF    : [] = [0, 0]#Flags: SZAPC
    __reg_BC    : [] = [0, 0]
    __reg_DE    : [] = [0, 0]
    __reg_HL    : [] = [0, 0]
    
    def get_reg(self, reg: ALU_Reg):
        match reg:
            case ALU_Reg.B: return self.__reg_BC[0]
            case ALU_Reg.C: return self.__reg_BC[1]
            case ALU_Reg.BC: return (self.__reg_BC[0] << 0x8) | self.__reg_BC[1]
            case ALU_Reg.D: return self.__reg_DE[0]
            case ALU_Reg.E: return self.__reg_DE[1]
            case ALU_Reg.DE: return (self.__reg_DE[0] << 0x8) | self.__reg_DE[1]
            case ALU_Reg.H: return self.__reg_HL[0]
            case ALU_Reg.L: return self.__reg_HL[1]
            case ALU_Reg.HL: return (self.__reg_HL[0] << 0x8) | self.__reg_HL[1]
            
    def set_reg(self, reg: ALU_Reg, val:int):
        match reg:
            case ALU_Reg.B: self.__reg_BC[0] = 0xFF & val
            case ALU_Reg.C: self.__reg_BC[1] = 0xFF & val
            case ALU_Reg.BC:
                self.__reg_BC[0] = 0xFF00 & val
                self.__reg_BC[1] = 0x00FF & val
            case ALU_Reg.D: self.__reg_DE[0] = 0xFF & val
            case ALU_Reg.E: self.__reg_DE[1] = 0xFF & val
            case ALU_Reg.DE:
                self.__reg_DE[0] = 0xFF00 & val
                self.__reg_DE[1] = 0x00FF & val 
            case ALU_Reg.H: self.__reg_HL[0] = 0xFF & val
            case ALU_Reg.L: self.__reg_HL[1] = 0xFF & val
            case ALU_Reg.HL:
                self.__reg_HL[0] = 0xFF00 & val
                self.__reg_HL[1] = 0x00FF & val         

    def get_acc(self):
        return self.__reg_AF[0]
    
    def set_acc(self, val: int):
        self.__reg_AF[0] = val & 0xFFFF

    def get_flag_sign(self):
        return self.__reg_AF[1] & 0x10

    def get_flag_zero(self):
        return self.__reg_AF[1] & 0x8
    
    def get_flag_aux(self):
        return self.__reg_AF[1] & 0x4
    
    def get_flag_parity(self):
        return self.__reg_AF[1] & 0x2

    def get_flag_carry(self):
        return self.__reg_AF[1] & 0x1
    
    def set_flags(self, sign: bool = None, zero: bool = None, aux: bool = None, parity: bool = None, carry: bool = None):
        if sign == True: self.__reg_AF[1] |= 0x10
        elif sign == False: self.__reg_AF[1] &= 0xF

        if zero == True: self.__reg_AF[1] |= 0x8
        elif zero == False: self.__reg_AF[1] &= 0x17

        if aux == True: self.__reg_AF[1] |= 0x4
        elif aux == False: self.__reg_AF[1] &= 0x1B

        if parity == True: self.__reg_AF[1] |= 0x2
        elif parity == False: self.__reg_AF[1] &= 0x1D

        if carry == True: self.__reg_AF[1] |= 0x1
        elif carry == False: self.__reg_AF[1] &= 0x1E

    def __init__(self, dec:Decoder) -> None:
        super().__init__()
        self.__dec = dec

class CPU(SharedCPU):

    clock   : Clock
    alu     : ALU

    def reset(self):
        self.inst_ptr = 0
        
    def __init__(self, mem:SharedMem, dec:Decoder) -> None:
        super().__init__(mem)

        self.clock = Clock()
        self.alu = ALU(dec)

