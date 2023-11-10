from Shared import ALU_Flag, ALU_Reg, SharedALU, SharedCPU, SharedCU, SharedMachine
from decoder import Decoder
from inst_info import ADDR_MODE, ITYPE

class ALU(SharedALU):

    __scpu      : SharedCPU
    __cmp       : SharedMachine
    __cu        : SharedCU
    __dec       : Decoder
    __reg_MA    : [] = [0, 0]
    __reg_BC    : [] = [0, 0]
    __reg_DE    : [] = [0, 0]
    __reg_HL    : [] = [0, 0]
    __flags     : [] = [False, False, False, False, False]
    
    def read_reg(self, reg: ALU_Reg):
        match reg:
            case ALU_Reg.M: return self.__reg_MA[0]
            case ALU_Reg.A: return self.__reg_MA[1]
            case ALU_Reg.B: return self.__reg_BC[0]
            case ALU_Reg.C: return self.__reg_BC[1]
            case ALU_Reg.D: return self.__reg_DE[0]
            case ALU_Reg.E: return self.__reg_DE[1]
            case ALU_Reg.H: return self.__reg_HL[0]
            case ALU_Reg.L: return self.__reg_HL[1]
            case _: print(f'ERROR: Register {reg.name} not a valid working register')

    def set_reg(self, reg: ALU_Reg, val: int):
        match reg:
            case ALU_Reg.M: self.__reg_MA[0] = val
            case ALU_Reg.A: self.__reg_MA[1] = val
            case ALU_Reg.B: self.__reg_BC[0] = val
            case ALU_Reg.C: self.__reg_BC[1] = val
            case ALU_Reg.D: self.__reg_DE[0] = val
            case ALU_Reg.E: self.__reg_DE[1] = val
            case ALU_Reg.H: self.__reg_HL[0] = val
            case ALU_Reg.L: self.__reg_HL[1] = val
            case _: print(f'ERROR: Register {reg.name} not a valid working register')
    
    def read_flag(self, flag: ALU_Reg):
        return self.__flags[flag.value]
    
    def set_flag(self, flag: ALU_Reg, val:int):
        self.__flags[flag.value-1] = val

    def read_direct(self, addr:int, two_reads:bool=False):
        hb = 0
        lb = self.__scpu.read_direct(1)
        if two_reads:
            hb = self.__scpu.read_direct(2)
        return (hb<<0x8)|lb

    #TODO worth keeping for sake of consistency?
    def is_parity(self, val:int, bytes:int): 
        sh = 1
        lim = 8 * bytes
        
        while sh <= lim:
            val ^= val >> sh
            sh = sh << 1
        return not val & 1

    def set_math_flags(self, res:int, lval:int, bytes:int, sub:bool=False):
        self.set_flag(ALU_Flag.S, res & 0x8000)
        self.set_flag(ALU_Flag.Z, res == 0)
        self.set_flag(ALU_Flag.A, res & 0x8000)
        self.set_flag(ALU_Flag.P, self.is_parity(res, bytes))
        self.set_flag(ALU_Flag.C, (lval >> 0x10) and not sub)

    #IO

    #INTERRUPT

    #CARRY

    #NOOP

    #SREG

    #DREG

    #ROTATE

    #DATA TRANSFER
    def __MOV(self, inst, mode:ADDR_MODE):
        src_c = (inst & 0x7) + 1
        dst_c =  ((inst & 0x38) >> 0x3) + 1
        src_val = self.read_reg(ALU_Reg(src_c))
        self.set_reg(ALU_Reg(dst_c), src_val)

    #REG/MEM TRANSFER
    def __ADD(self, inst, mode:ADDR_MODE):
        src_c = (inst & 0x7) + 1
        src_val = self.read_reg(ALU_Reg(src_c))
        acc_val = self.read_reg(ALU_Reg.A)
        res = acc_val = acc_val + src_val
        self.set_reg(ALU_Reg.A, res)
        self.set_math_flags(res, acc_val, 2)

    def __SUB(self, inst, mode:ADDR_MODE):
        src_c = (inst & 0x7) + 1
        src_val = self.read_reg(ALU_Reg(src_c))
        acc_val = self.read_reg(ALU_Reg.A)
        res = acc_val = acc_val + src_val
        self.set_math_flags(res, acc_val, 2)

    #DIRECT ADDR
    def __LDA(self, inst:int, mode:ADDR_MODE):
        addr = 0
        if mode == ADDR_MODE.IMMEDIATE:
            addr = self.read_direct(self.__scpu.mar, True)
        val = self.__cu.read_mem(addr)
        self.set_reg(ALU_Reg.A, val)

    def __STA(self, inst:int, mode:ADDR_MODE):
        addr = 0
        acc = self.read_reg(ALU_Reg.A)
        if mode == ADDR_MODE.IMMEDIATE:
            addr = self.read_direct(self.__scpu.mar, True)
        self.__scpu.set_word(acc, addr)

    #IMM

    #JUMP
    def __JMP(self, inst, mode:ADDR_MODE):
        addr = 0
        if mode == ADDR_MODE.IMMEDIATE:
            addr = self.read_direct(self.__scpu.mar, True)
        self.__scpu.jmp_addr(addr)

    #CALL

    #RETURN

    def execute(self, inst:int):
        itype, addrm, mod = self.__dec.decode_inst(inst)
        
        print(f'EXEC: {inst:#08b} : {itype.name:<6}   {addrm.name}')

        match itype:
            case ITYPE.LDA: self.__LDA(inst, addrm)
            case ITYPE.STA: self.__STA(inst, addrm)
            
            case ITYPE.ADD: self.__ADD(inst, addrm)

            case ITYPE.MOV: self.__MOV(inst, addrm)

            case ITYPE.JMP: self.__JMP(inst, addrm)

            case _:
                print(f'WARNING: Unrecognized instruction "{itype}"')

        self.__cmp.update_display()
        

    def set_cu(self, cu:SharedCU):
        self.__cu = cu

    def __init__(self, dec:Decoder, scpu:SharedCPU, scmp:SharedMachine) -> None:
        super().__init__()
        self.__cmp = scmp
        self.__dec = dec
        self.__scpu = scpu

