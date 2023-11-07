from Shared import ALU_Reg, SharedALU, SharedCPU
from decoder import Decoder
from inst_info import ADDR_MODE, ITYPE

class ALU(SharedALU):

    __scpu      : SharedCPU
    __dec       : Decoder
    __reg_AF    : [] = [0, 0]#Flags: SZAPC
    __reg_BC    : [] = [0, 0]
    __reg_DE    : [] = [0, 0]
    __reg_HL    : [] = [0, 0]
    
    #IO

    #INTERRUPT

    #CARRY

    #NOOP

    #SREG

    #DREG

    #ROTATE

    #DATA TRANSFER
    def __MOV(self, inst):
        pass

    #REG/MEM TRANSFER
    def __ADD(self, inst):
        pass

    #DIRECT ADDR
    def __LDAX(self, inst:int, mode:ADDR_MODE):
        addr = self.get_reg(ALU_Reg.HL)
    def __STAX(self, inst:int, mode:ADDR_MODE):
        pass

    #IMM

    #JUMP
    def __JMP(self, inst):
        pass

    #CALL

    #RETURN

    def execute(self, inst:int):
        itype, addrm = self.__dec.decode_inst(inst)
        
        f'EXEC: {inst:#08b} : {itype.name:<6}   {addrm.name}'

        match itype:
            case ITYPE.LDAX: self.__LDAX(inst, addrm)
            case ITYPE.STAX: self.__STAX(inst, addrm)
            
            case ITYPE.ADD: self.__ADD(inst)

            case ITYPE.MOV: self.__MOV(inst)

            case ITYPE.JMP: self.__JMP(inst)

            case _:
                print(f'WARNING: Unrecognized instruction "{itype}"')

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

    def __init__(self, dec:Decoder, scpu:SharedCPU) -> None:
        super().__init__()
        self.__dec = dec
        self.__scpu = scpu
