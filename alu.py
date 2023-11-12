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
    
    def reg_pair(self, code):
        match code:
            case 0x0: return ALU_Reg.BC
            case 0x1: return ALU_Reg.DE
            case 0x2: return ALU_Reg.HL
            case 0x3: return ALU_Reg.MA

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
            case ALU_Reg.BC: return self.__reg_BC[0] | self.__reg_BC[1] << 8
            case ALU_Reg.DE: return self.__reg_DE[0] | self.__reg_DE[1] << 8
            case ALU_Reg.HL: return self.__reg_HL[0] | self.__reg_HL[1] << 8
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
            case ALU_Reg.BC: 
                self.__reg_BC[0] = val & 0x00FF
                self.__reg_BC[1] = val & 0xFF00
            case ALU_Reg.DE: 
                self.__reg_DE[0] = val & 0x00FF
                self.__reg_DE[1] = val & 0xFF00
            case ALU_Reg.HL: 
                self.__reg_HL[0] = val & 0x00FF
                self.__reg_HL[1] = val & 0xFF00            
            case _: print(f'ERROR: Register {reg.name} not a valid working register')
    
    def read_flag(self, flag: ALU_Flag):
        return self.__flags[flag.value]
    
    def set_flag(self, flag: ALU_Flag, val:int):
        self.__flags[flag.value-1] = val

    def read_direct(self, addr:int, two_reads:bool=False):
        hb = 0
        lb = self.__scpu.read_direct(1)
        if two_reads:
            hb = self.__scpu.read_direct(2)
        return (hb<<0x8)|lb

    def write_direct(self, addr:int, data:int, two_writes:bool=False):
        lb = data&0x00FF
        hb = data&0xFF00
        self.__scpu.write_direct(1, lb)
        if two_writes:
            self.__scpu.write_direct(2, hb)


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
    def __OUT(self, inst:int):
        addr = self.read_direct(self.__scpu.mar, False)
        #TODO Send to dev. no
    
    def __IN(self, inst:int):
        addr = self.read_direct(self.__scpu.mar, False)
        #TODO load from dev. no

    #DATA TRANSFER
    def __MOV(self, inst, mode:ADDR_MODE):

        src_c = 0
        dst_c = 0

        if mode == ADDR_MODE.IMMEDIATE:
            src_c = (inst & 0x7) + 1
            dst_c =  ((inst & 0x38) >> 0x3) + 1
            src_val = self.read_reg(ALU_Reg(src_c))
        else:
            src_val = self.read_direct(self.__cpu.mar, False)
            dst_c = (inst>>3)&0x7
        
        self.set_reg(ALU_Reg(dst_c), src_val)

    def __XCHG(self):
        tmp = self.read_reg(ALU_Reg.HL)
        self.set_reg(ALU_Reg.HL, self.read_reg(ALU_Reg.DE))
        self.set_reg(ALU_Reg.DE, tmp)

    def __LHLD(self, inst):
        val = self.read_direct(self.__scpu.mar, True)
        self.set_reg(ALU_Reg.HL, val)

    def __SHLD(self, inst):
        val = self.read_reg(ALU_Reg.HL)
        self.write_direct(self.__scpu.mar, val, True)


    def __SPHL(self, inst):
        val = self.read_reg(ALU_Reg.HL)
        self.__scpu.stck_ptr = val

    #REGISTER MODIFY
    def __INR(self, inst, mod:int):
        if mod == 1:  reg = self.reg_pair((inst>>4) & 0x3)
        else: reg = ALU_Reg((inst>>3)&0x7)

        val = self.read_reg(reg)
        self.set_reg(reg, val+1)

    def __DCR(self, inst, mod:int):
        if mod == 1:  reg = self.reg_pair((inst>>4) & 0x3)
        else: reg = ALU_Reg((inst>>3)&0x7)

        val = self.read_reg(reg)
        self.set_reg(reg, val-1)

    #REG/MEM TRANSFER
    def __ADD(self, inst:int, mode:ADDR_MODE):

        acc_val = self.read_reg(ALU_Reg.A)
        val = 0

        if mode == ADDR_MODE.DIRECT:
            val = self.read_direct(self.__scpu.mar)
        else:
            src_c = (inst & 0x7) + 1
            val = self.read_reg(ALU_Reg(src_c))
            
        res  = acc_val + val
        self.set_reg(ALU_Reg.A, res)
        self.set_math_flags(res, acc_val, 2)

    def __SUB(self, inst:int, mode:ADDR_MODE):

        acc_val = self.read_reg(ALU_Reg.A)
        val = 0

        if mode == ADDR_MODE.DIRECT:
            val = self.read_direct(self.__scpu.mar)
        else:
            src_c = (inst & 0x7) + 1
            val = self.read_reg(ALU_Reg(src_c))
        
        res = acc_val - val
        self.set_reg(ALU_Reg.A, res)
        self.set_math_flags(res, acc_val, 2, True)

    def __AND(self, inst, addrm):
        
        val = 0
        acc = self.read_reg(ALU_Reg.A)

        if addrm == ADDR_MODE.IMMEDIATE:
            val = self.read_direct(self.__scpu.get_mar())
        else:
            val = self.read_reg(ALU_Reg(inst&0x7))

        res = val & acc

        self.set_flag(ALU_Flag.C, False)
        self.set_flag(ALU_Flag.P, self.is_parity(res))
        self.set_flag(ALU_Flag.Z, res == 0)
        self.set_flag(ALU_Flag.S, res < 0)

    def __OR(self, inst, addrm):
        val = 0
        acc = self.read_reg(ALU_Reg.A)

        if addrm == ADDR_MODE.IMMEDIATE:
            val = self.read_direct(self.__scpu.get_mar())
        else:
            val = self.read_reg(ALU_Reg(inst&0x7))

        res = val | acc

        self.set_flag(ALU_Flag.C, False)
        self.set_flag(ALU_Flag.P, self.is_parity(res))
        self.set_flag(ALU_Flag.Z, res == 0)
        self.set_flag(ALU_Flag.S, res < 0)
    
    def __XOR(self, inst, addrm):
        val = 0
        acc = self.read_reg(ALU_Reg.A)

        if addrm == ADDR_MODE.IMMEDIATE:
            val = self.read_direct(self.__scpu.get_mar())
        else:
            val = self.read_reg(ALU_Reg(inst&0x7))

        res = val ^ acc

        self.set_flag(ALU_Flag.C, False)
        self.set_flag(ALU_Flag.P, self.is_parity(res))
        self.set_flag(ALU_Flag.Z, res == 0)
        self.set_flag(ALU_Flag.S, res < 0)

    #ACCUMLATOR
    def __LDA(self, inst:int, mode:ADDR_MODE, mod:int):
        addr = 0
        if mode == ADDR_MODE.IMMEDIATE:
            addr = self.read_direct(self.__scpu.mar, True)
            val = self.__cu.read_mem(addr)
        else:
            reg = ALU_Reg.BC if mod == 0 else ALU_Reg.DE
            val = self.read_reg(reg)

        self.set_reg(ALU_Reg.A, val)

    def __STA(self, inst:int, mode:ADDR_MODE, mod:int):
        addr = 0
        acc = self.read_reg(ALU_Reg.A)
        if mode == ADDR_MODE.IMMEDIATE:
            addr = self.read_direct(self.__scpu.mar, True)
            self.__scpu.set_word(acc, addr)
        else:
            reg = ALU_Reg.BC if mod == 0 else ALU_Reg.DE
            self.set_reg(reg, acc)

    def __ROT(self, inst:int, mod:int):
        acc = self.read_reg(ALU_Reg.A)
        c = self.read_flag(ALU_Flag.C)
        b7 = acc&0x80
        b0 = acc&0x01
        if mod == 0: #RLC
            acc = (acc << 1) | b7 >> 7
            c = b7
        elif mod == 2: #RRC
            acc = (acc >> 1) | b0 << 7
            c = b0
        elif mod == 3: #RAL
            acc = (acc << 1) | c
            c = b7
        elif mod == 4: #RAR
            acc = (acc >> 1) | c << 7
            c = b0

        self.set_flag(ALU_Flag.C, b7)

    #CTRL
    def __HALT(self, inst):
        self.__cu.halt()

    def __RESET(self, inst):
        addr = inst & 0x38
        self.__scpu.push_stack(self.__scpu.get_instr())
        self.__scpu.set_addr(addr)

    #COMPARE
    def __CMP(self, inst):
        src_c = (inst & 0x7) + 1
        src_val = self.read_reg(ALU_Reg(src_c))
        acc_val = self.read_reg(ALU_Reg.A)
        diff = acc_val - src_val

        self.set_flag(ALU_Flag.Z, diff==0)
        self.set_flag(ALU_Flag.C, src_val > acc_val) #TODO Check sense if sign mismatch
        self.set_flag(ALU_Flag.S, diff < 0)
        self.set_flag(ALU_Flag.P, self.is_parity(diff, 1))

    #JUMP
    def __JMP(self, inst):

        jmp = False

        match inst:
            case 0xC3: jmp = True #JMP
            case 0xF2: jmp = self.read_flag(ALU_Flag.S) == 0 #JP
            case 0xFA: jmp = self.read_flag(ALU_Flag.S) == 1 #JM
            case 0xCA: jmp = self.read_flag(ALU_Flag.Z) == 1 #JZ
            case 0xC2: jmp = self.read_flag(ALU_Flag.Z) == 0 #JNZ
            case 0xDA: jmp = self.read_flag(ALU_Flag.C) == 1 #JC
            case 0xD2: jmp = self.read_flag(ALU_Flag.C) == 0 #JNC
            case 0xEA: jmp = self.read_flag(ALU_Flag.P) == 1 #JPE
            case 0xE2: jmp = self.read_flag(ALU_Flag.P) == 0 #JPO
            
        if not jmp: return

        addr = self.read_direct(self.__scpu.mar, True)
        self.__scpu.jmp_addr(addr)

    #CALL
    def __CALL(self, inst:int):
        
        call = False

        match inst:
            case 0xCD: call = True #CALL
            case 0xF4: call = self.read_flag(ALU_Flag.S) == 0 #CP
            case 0xFC: call = self.read_flag(ALU_Flag.S) == 1 #CM
            case 0xCC: call = self.read_flag(ALU_Flag.Z) == 1 #CZ
            case 0xC4: call = self.read_flag(ALU_Flag.Z) == 0 #CNZ
            case 0xDC: call = self.read_flag(ALU_Flag.C) == 1 #CC
            case 0xD4: call = self.read_flag(ALU_Flag.C) == 0 #CNC
            case 0xEC: call = self.read_flag(ALU_Flag.P) == 1 #CPE
            case 0xE4: call = self.read_flag(ALU_Flag.P) == 0 #CPO

        if not call: return

        self.__scpu.push_stack(self.__scpu.inst_ptr)
        addr = self.read_direct(self.__scpu.mar, True)
        self.__scpu.jmp_addr(addr)

    #RETURN

    def __RET(self, inst:int):
        
        ret = False

        match inst:
            case 0xCD: ret = True #CALL
            case 0xF0: ret = self.read_flag(ALU_Flag.S) == 0 #RP
            case 0xF8: ret = self.read_flag(ALU_Flag.S) == 1 #RM
            case 0xC8: ret = self.read_flag(ALU_Flag.Z) == 1 #RZ
            case 0xC0: ret = self.read_flag(ALU_Flag.Z) == 0 #RNZ
            case 0xD8: ret = self.read_flag(ALU_Flag.C) == 1 #RC
            case 0xD0: ret = self.read_flag(ALU_Flag.C) == 0 #RNC
            case 0xE8: ret = self.read_flag(ALU_Flag.P) == 1 #RPE
            case 0xE0: ret = self.read_flag(ALU_Flag.P) == 0 #RPO

        if not ret: return

        addr = self.__scpu.pop_stack()
        self.__scpu.jmp_addr(addr)



    def execute(self, inst:int):
        itype, addrm, mod = self.__dec.decode_inst(inst)
        
        print(f'EXEC: {inst:#08b} : {itype.name:<6}   {addrm.name}')

        match itype:
            case ITYPE.IN: self.__IN(inst)
            case ITYPE.OUT: self.__OUT(inst)

            case ITYPE.LDA: self.__LDA(inst, addrm, mod)
            case ITYPE.STA: self.__STA(inst, addrm, mod)
            case ITYPE.ROT: self.__ROT(inst, mod)
            
            case ITYPE.LHLD: self.__LHLD(inst)
            case ITYPE.SPHL: self.__SPHL(inst)
            case ITYPE.SHLD: self.__SHLD(inst)
            
            case ITYPE.ADD: self.__ADD(inst, addrm)
            case ITYPE.SUB: self.__SUB(inst, addrm)

            case ITYPE.AND: self.__AND(inst, addrm)
            case ITYPE.OR: self.__OR(inst, addrm)
            case ITYPE.XOR: self.__XOR(inst, addrm)

            case ITYPE.MOV: self.__MOV(inst, addrm)
            case ITYPE.XCHG: self.__XCHG()

            case ITYPE.INX: self.__INR(inst, mod)
            case ITYPE.DCX: self.__DCR(inst, mod)

            case ITYPE.HALT: self.__HALT(inst)
            case ITYPE.RESET: self.__RESET(inst)

            case ITYPE.CALL: self.__CALL(inst)
            case ITYPE.RETURN: self.__RET(inst)
            case ITYPE.JMP: self.__JMP(inst)

            case ITYPE.CMP: self.__CMP(inst)

            case ITYPE.RESET: self.__RESET(inst)

            case ITYPE.NOP: pass

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


