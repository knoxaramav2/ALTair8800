from inst_info import ADDR_MODE, ITYPE

class Decoder:
    
    def inst_len(self, inst:int):
        ln = 1

        hb = (inst & 0xF0) >> 4
        lb = inst & 0x0F

        if hb <= 0x3:
            if lb == 0x1: ln = 3
            elif lb == 0x2 and hb >= 0x2: ln = 3
            elif lb == 0x6: ln = 2
            elif lb == 0xA and hb >= 0x2: ln = 3
            elif lb == 0xE: ln = 2
        elif hb >= 0xC:
            if lb == 0x2: ln = 3
            elif lb == 0x3 and hb == 0xC: ln = 3
            elif lb == 0x3 and hb == 0xD: ln = 2
            elif lb == 0x4: ln = 3
            elif lb == 0x6: ln = 2
            elif lb == 0xA: ln = 3
            elif lb == 0xB and hb == 0xD: ln = 2
            elif lb == 0xC or lb == 0xD: ln = 3
            elif lb == 0xE: ln = 2

        return ln

    def decode_inst(self, inst:int) -> [ITYPE, ADDR_MODE, int]:
        
        addrm   : ADDR_MODE = ADDR_MODE.REGISTER
        itype    : ITYPE = ITYPE.NOP
        hb = inst >> 0x4
        lb = inst & 0xF
        mod = 0

        if (hb >= 0x0 and hb <= 0x4) and (lb == 0x1 or lb == 0x6 or lb == 0xE):
            itype = ADDR_MODE.IMMEDIATE
        elif (hb == 0x2 or hb == 0x3) and (lb == 0x2 or lb == 0xA):
            itype == ADDR_MODE.DIRECT
        
        if (hb >= 0x0 and hb <= 0x3):
            if (lb == 0x1): itype = ITYPE.LXI
            elif (lb == 0x2):
                addrm = ADDR_MODE.IMMEDIATE
                if (hb == 0x2): itype = ITYPE.SHLD
                else: 
                    itype = ITYPE.STA
                    mod = hb
                    if hb <= 0x1: addrm = ADDR_MODE.REGISTER
            elif (lb == 0x3 or lb == 0x4 or lb == 0xC): 
                if lb == 0x3: mode = 1
                itype = ITYPE.INX
            elif (lb == 0x5 or lb == 0xB or lb == 0xD): 
                if lb == 0xB: mod = 1
                itype = ITYPE.DCX
            elif (lb == 0x6 or lb == 0xE): itype = ITYPE.MVI
            elif (lb == 0x7 or lb == 0xF): 
                if (hb == 0x0 or hb == 0x1):
                    itype = ITYPE.ROT
                    mod = hb
                elif (hb == 0x3): 
                    itype = ITYPE.ACCU
                    mod = int(hb == 0x7)
                else:
                    itype = ITYPE.CARRY
                    mod = int(hb == 0x7)
            elif (lb == 0x9): itype = ITYPE.DAD
            elif (lb == 0xA):
                addrm = ADDR_MODE.IMMEDIATE
                if (hb == 0x2): itype = ITYPE.LHLD
                else: 
                    if hb <= 1: addrm = ADDR_MODE.REGISTER
                    itype = ITYPE.LDA
                    
        elif (hb >= 0x4 and hb <= 0x7):
            if (lb == 0x6): itype = ITYPE.HALT
            else: itype = ITYPE.MOV
        elif (hb == 0x8):
            itype = ITYPE.ADD
            mod = int(lb < 0x8)
        elif (hb == 0x9):
            itype = ITYPE.SUB
            mod = int(lb < 0x8)
        elif (hb == 0xA):
            if (lb < 0x8): itype = ITYPE.AND
            else: itype = ITYPE.XOR
        elif (hb == 0xB):
            if (lb < 0x8): itype = ITYPE.OR
            else: itype = ITYPE.CMP
        else:#C-F
            if (lb == 0x0):
                itype = ITYPE.RETURN
                mod = hb - 0xC
            elif(lb == 0x1): itype = ITYPE.POP
            elif (lb == 0x2 or lb == 0x3 or lb == 0xA):
                if (lb == 0x3 and hb == 0xD): itype = ITYPE.OUT
                elif (lb == 0x3 and hb == 0xE): itype = ITYPE.XTHL
                elif (lb == 0x3 and hb == 0xF): itype = ITYPE.DI
                else:
                    itype = ITYPE.JMP
                    addrm = ADDR_MODE.IMMEDIATE
                    mod = (hb<<2&0xC)|(lb&0x3)
            elif (lb == 0x4 or lb == 0xC or lb == 0xD):
                itype == ITYPE.CALL
                mod = (hb<<2&0xC)|(lb>>2&0x2|lb&0x1)
                addrm = ADDR_MODE.IMMEDIATE
            elif (lb == 0x5): pass #PUSH
            elif (lb == 0x6): pass
            elif (lb == 0x7): pass
            elif (lb == 0x8): pass
            elif (lb == 0x9): pass
            elif (lb == 0xB): pass
            elif (lb == 0xE): pass
            elif (lb == 0xF): pass

        return itype, addrm, mod


    def __init__(self) -> None:
        pass