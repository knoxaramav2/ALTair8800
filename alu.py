from Shared import ALU_Flag, ALU_Reg, SharedALU, SharedCPU, SharedCU, SharedMachine
from decoder import ADDRM, OP, OPCODE, Decoder

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
        return self.__flags[flag.value-1]
    
    def set_flag(self, flag: ALU_Flag, val:int):
        self.__flags[flag.value-1] = val

    def read_direct(self, addr:int=None, two_reads:bool=False):
        if addr == None: addr = self.__scpu.get_mar()
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
    def __OUT(self, op:OP):
        addr = self.read_direct()
        #TODO Send to dev. no
    
    def __IN(self, op:OP):
        addr = self.read_direct()
        #TODO load from dev. no

    #DATA TRANSFER
    def __MOV(self, op:OP):

        src_c = 0
        dst_c = 0

        if op.addrm == ADDRM.IMM:
            src_c = (op.nst & 0x7) + 1
            dst_c =  ((op.inst & 0x38) >> 0x3) + 1
            src_val = self.read_reg(ALU_Reg(src_c))
        elif op.addrm == ADDRM.REG:
            src_val = self.read_direct()
            dst_c = ((op.inst>>3)&0x7) + 1
        
        self.set_reg(ALU_Reg(dst_c), src_val)

    def __XCHG(self, op:OP):
        tmp = self.read_reg(ALU_Reg.HL)
        self.set_reg(ALU_Reg.HL, self.read_reg(ALU_Reg.DE))
        self.set_reg(ALU_Reg.DE, tmp)

    def __LHLD(self, op:OP):
        val = self.read_direct(two_reads=True)
        self.set_reg(ALU_Reg.HL, val)

    def __SHLD(self, op:OP):
        val = self.read_reg(ALU_Reg.HL)
        addr = self.read_direct(two_reads=True)
        self.write_direct(addr, val, True)


    def __SPHL(self, op:OP):
        val = self.read_reg(ALU_Reg.HL)
        self.__scpu.stck_ptr = val

    def __XTHL(self, op:OP):
        
        hl = self.read_reg(ALU_Reg.HL)
        sv = self.read_direct(self.__scpu.stck_ptr-2, True)
        self.set_reg(ALU_Reg.HL, sv)
        self.write_direct(self.__scpu.stck_ptr, hl, True)

    #REGISTER MODIFY
    def __INR(self, op:OP):
        
        val = 0
        reg = None

        if op.alt == 0: reg = self.read_reg(ALU_Reg((op.inst>>3&0x7)+1))
        elif op.alt == 1: reg =self.reg_pair(op.inst>>4&0x3) 

        val = self.read_reg(reg)
        self.set_reg(reg, val+1)

    def __DCR(self, op:OP):
        
        val = 0
        reg = None

        if op.alt == 0: reg = self.read_reg(ALU_Reg((op.inst>>3&0x7)+1))
        elif op.alt == 1: reg =self.reg_pair(op.inst>>4&0x3) 

        val = self.read_reg(reg)
        self.set_reg(reg, val-1)

    def __CRA(self, op:OP):
        
        if op.alt == 0: self.set_flag(ALU_Flag.C, True)#STC
        elif op.alt == 1: 
            c = self.read_flag(ALU_Flag.C)
            self.set_flag(ALU_Flag.C, 1-c)

    def __AAC(self, op:OP):
        
        val = self.read_reg(ALU_Reg.A)

        if op.alt == 0:#DAA
            val&=0xFF
            v1 = (val & 0xF0) >> 4
            v2 = val & 0x0F
            if v2 > 0x9 or self.read_flag(ALU_Flag.A): v2 += 6
            self.set_flag(ALU_Flag.A, v2&0x10)
            if v1 > 0x9 or self.read_flag(ALU_Flag.A): v1 += 6
            self.set_flag(ALU_Flag.A, v1&0x10)
        elif op.alt == 1:#CMA
            val ^= 0xFF

        self.set_reg(ALU_Reg.A, val)


    def __POP(self, op:OP):
        val = self.__scpu.pop_stack()
        reg = self.reg_pair(op.inst>>4&0x3)
        self.set_reg(reg, val)

    def __PUSH(self, op:OP):
        reg = self.reg_pair(op.inst>>4&0x3)
        val = self.read_reg(reg)
        self.__scpu.push_stack(val)

    #REG/MEM TRANSFER
    def __ADD(self, op:OP):

        acc_val = self.read_reg(ALU_Reg.A)
        val = 0
        c = 0

        if op.addrm == ADDRM.IMM: val = self.read_direct()
        elif op.addrm == ADDRM.REG: 
            if op.alt == 2: val = self.read_reg(self.reg_pair((op.inst>>4)&0x3))
            else: val = self.read_reg(ALU_Reg((op.inst&0x7)+1))

        if op.alt == 1: c = self.read_flag(ALU_Flag.C)

        res = acc_val + val + c

        self.set_reg(ALU_Reg.A, res)
        self.set_math_flags(res, acc_val, 2)

    def __SUB(self, op:OP):

        acc_val = self.read_reg(ALU_Reg.A)
        val = 0
        c = 0

        if op.addrm == ADDRM.IMM: val = self.read_direct()
        elif op.addrm == ADDRM.REG: 
            if op.alt == 2: val = self.read_reg(self.reg_pair((op.inst>>4)&0x3))
            else: val = self.read_reg(ALU_Reg((op.inst&0x7)+1))

        if op.alt == 1: c = self.read_flag(ALU_Flag.C)

        res = acc_val - (val + c)

        self.set_reg(ALU_Reg.A, res)
        self.set_math_flags(res, acc_val, 2)

    def __ALG(self, op:OP):
        val = 0
        acc = self.read_reg(ALU_Reg.A)

        if op.addrm == ADDRM.IMM: val = self.read_direct()
        else: val = self.read_reg(ALU_Reg(op.inst&0x7))

        if op.alt == 0: val = val & acc
        elif op.alt == 1: val = val ^ acc
        elif op.alt == 2: val = val | acc

        self.set_flag(ALU_Flag.C, False)
        self.set_flag(ALU_Flag.P, self.is_parity(val))
        self.set_flag(ALU_Flag.Z, val == 0)
        self.set_flag(ALU_Flag.S, val < 0)

    #ACCUMLATOR
    def __LDA(self, op:OP):
        addr = 0

        if op.addrm == ADDRM.DIR:
            addr = self.read_direct(self.__scpu.mar, True)
            val = self.__cu.read_mem(addr)
        elif op.addrm == ADDRM.REG:
            reg = ALU_Reg.BC if op.inst&0x10 == 0 else ALU_Reg.DE
            val = self.read_reg(reg)

        self.set_reg(ALU_Reg.A, val)

    def __STA(self, op:OP):
        addr = 0
        acc = self.read_reg(ALU_Reg.A)
        if op.addrm == ADDRM.DIR:
            addr = self.read_direct(self.__scpu.mar, True)
            self.__scpu.set_word(acc, addr)
        else:
            reg = ALU_Reg.BC if op.inst&10 == 0 else ALU_Reg.DE
            self.set_reg(reg, acc)

    def __LXI(self, op:OP):
        reg = self.reg_pair(op.inst>>4&0x3)
        val = self.read_direct(two_reads=True)
        if reg == ALU_Reg.MA:
            self.__scpu.stck_ptr = val
            return
        self.set_reg(reg, val)

    def __ROT(self, op:OP):
        acc = self.read_reg(ALU_Reg.A)
        c = self.read_flag(ALU_Flag.C)
        b7 = acc&0x80
        b0 = acc&0x01
        
        if op.alt == 0:  #RLC
            acc = (acc << 1) | (b7 >> 7)
            self.set_flag(ALU_Flag.C, b7)
        elif op.alt == 1:#RAL
            acc = (acc << 1) | c
            self.set_flag(ALU_Flag.C, b7)
        elif op.alt == 2:#RRC
            acc = (acc >> 1) | (b0 << 7)
            self.set_flag(ALU_Flag.C, b0)
        elif op.alt == 3:#RAR
            acc = (acc >> 1) | c
            self.set_flag(ALU_Flag.C, b0)

        self.set_reg(ALU_Reg.A, acc)

    #CTRL
    def __HALT(self, op:OP):
        self.__cu.halt()

    def __RESET(self, op:OP):
        addr = op.inst & 0x38
        self.__scpu.push_stack(self.__scpu.get_instr())
        self.__scpu.set_addr(addr)

    def __INT(self, op:OP):
        self.__scpu.inte.set(op.alt)

    #COMPARE
    def __CMP(self, op:OP):

        val = 0
        acc = self.read_reg(ALU_Reg.A)

        if op.addrm == ADDRM.IMM: val = self.read_direct()
        elif op.addrm == ADDRM.REG: val = self.read_reg(ALU_Reg((op.inst&0x7)+1))

        diff = acc - val
        print(f'CMP: {acc:02x}/{val:02x}')

        self.set_flag(ALU_Flag.Z, diff==0)
        self.set_flag(ALU_Flag.C, val > acc) #TODO Check sense if sign mismatch
        self.set_flag(ALU_Flag.S, diff < 0)
        self.set_flag(ALU_Flag.P, self.is_parity(diff, 1))

    #JUMP
    def __JMP(self, op:OP):

        jmp = False

        match op.alt:
            case 0x0: jmp = True #JMP
            case 0x1: jmp = self.read_flag(ALU_Flag.Z) == 0 #JNZ
            case 0x2: jmp = self.read_flag(ALU_Flag.Z) == 1 #JZ
            case 0x3: jmp = self.read_flag(ALU_Flag.S) == 0 #JP
            case 0x4: jmp = self.read_flag(ALU_Flag.S) == 1 #JM
            case 0x5: jmp = self.read_flag(ALU_Flag.C) == 0 #JNC
            case 0x6: jmp = self.read_flag(ALU_Flag.C) == 1 #JC
            case 0x7: jmp = self.read_flag(ALU_Flag.P) == 0 #JPO
            case 0x8: jmp = self.read_flag(ALU_Flag.P) == 1 #JPE
            
        if not jmp: return

        addr = self.read_direct(self.__scpu.mar, True)
        self.__scpu.jmp_addr(addr)

    #CALL
    def __CALL(self, op:OP):
        
        call = False

        match op.alt:
            case 0x0: call = True #CALL
            case 0x1: call = self.read_flag(ALU_Flag.Z) == 0 #CNZ
            case 0x2: call = self.read_flag(ALU_Flag.Z) == 1 #CZ
            case 0x3: call = self.read_flag(ALU_Flag.C) == 0 #CNC
            case 0x4: call = self.read_flag(ALU_Flag.C) == 1 #CC
            case 0x5: call = self.read_flag(ALU_Flag.P) == 0 #CPO
            case 0x6: call = self.read_flag(ALU_Flag.P) == 1 #CPE
            case 0x7: call = self.read_flag(ALU_Flag.S) == 0 #CP
            case 0x8: call = self.read_flag(ALU_Flag.S) == 1 #CM

        if not call: return

        self.__scpu.push_stack(self.__scpu.inst_ptr)
        addr = self.read_direct(self.__scpu.mar, True)
        self.__scpu.jmp_addr(addr)

    #RETURN
    def __RET(self, op:OP):
        
        ret = False

        match op.alt:
            case 0x0: ret = True #CALL
            case 0x1: ret = self.read_flag(ALU_Flag.Z) == 0 #RNZ
            case 0x2: ret = self.read_flag(ALU_Flag.Z) == 1 #RZ
            case 0x3: ret = self.read_flag(ALU_Flag.C) == 0 #RNC
            case 0x4: ret = self.read_flag(ALU_Flag.C) == 1 #RC
            case 0x5: ret = self.read_flag(ALU_Flag.P) == 0 #RPO
            case 0x6: ret = self.read_flag(ALU_Flag.P) == 1 #RPE
            case 0x7: ret = self.read_flag(ALU_Flag.S) == 0 #RP
            case 0x8: ret = self.read_flag(ALU_Flag.S) == 1 #RM
        
        if not ret: return

        addr = self.__scpu.pop_stack()
        self.__scpu.jmp_addr(addr)



    def execute(self, inst:int):
        op = self.__dec.decode_inst(inst)
        
        print(f'EXEC: {inst:#08b} : {op.name:<6}   {op.addrm.name}')

        match op.opcode:
            case OPCODE.IN: self.__IN(op)#TBD
            case OPCODE.OUT: self.__OUT(op)#TDB

            case OPCODE.INT: self.__INT(op)#Check

            case OPCODE.LDA: self.__LDA(op)#Check
            case OPCODE.STA: self.__STA(op)#Check
            case OPCODE.LXI: self.__LXI(op)#Check
            case OPCODE.LHLD: self.__LHLD(op)#Check
            case OPCODE.SHLD: self.__SHLD(op)#Check
            case OPCODE.SPHL: self.__SPHL(op)#Check
            case OPCODE.XTHL: self.__XTHL(op)#Check
            case OPCODE.XCHG: self.__XCHG()#Check
            case OPCODE.MOV: self.__MOV(op)#Check

            case OPCODE.ADD: self.__ADD(op)#Check
            case OPCODE.SUB: self.__SUB(op)#Check
            case OPCODE.ALG: self.__ALG(op)#Check

            case OPCODE.ROT: self.__ROT(op)#Check
            case OPCODE.CMP: self.__CMP(op)#Check

            case OPCODE.JMP: self.__JMP(op)#Check
            case OPCODE.CALL: self.__CALL(op)#Check
            case OPCODE.RET: self.__RET(op)#Check

            case OPCODE.HALT: self.__HALT(op)#Check
            case OPCODE.RST: self.__RESET(op)#Check

            case OPCODE.INR: self.__INR(op)#Check
            case OPCODE.DCR: self.__DCR(op)#Check

            case OPCODE.CRA: self.__CRA(op)#Check
            case OPCODE.AAC: self.__AAC(op)#Check

            case OPCODE.POP: self.__POP(op)#Check
            case OPCODE.PUSH: self.__PUSH(op)#Check

            case OPCODE.NOP: pass

            case _:
                print(f'WARNING: Unrecognized instruction "{op.opcode}"')

        self.__cmp.update_display()
        

    def set_cu(self, cu:SharedCU):
        self.__cu = cu

    def __init__(self, dec:Decoder, scpu:SharedCPU, scmp:SharedMachine) -> None:
        super().__init__()
        self.__cmp = scmp
        self.__dec = dec
        self.__scpu = scpu


