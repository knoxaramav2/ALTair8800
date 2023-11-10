from inst_info import ADDR_MODE, ITYPE

class Decoder:
    
    def inst_len(self, inst:int):
        ln = 1

        hb = inst & 0xF0
        lb = inst & 0xF

        #TODO Make this less clunky
        match lb:
            case 1: 
                if hb <= 0x3: ln = 3
            case 2:
                if hb >= 0xC: ln = 3
            case 3:
                if hb == 0xC: ln = 3
            case 4:
                if hb >= 0xC: ln = 3
            case 0xA:
                if (hb == 0x1 or hb == 0x2) or (hb >= 0xC): ln = 3
            case 0xC:
                if hb >= 0xC: ln = 3
            case 0xD:
                if hb == 0xC: ln = 3
            case 0x3:
                if hb == 0xD: ln = 2
            case 0x6:
                if (hb >= 0x0 and hb <= 0x3) or (hb >= 0xC): ln = 2
            case 0xB:
                if hb == 0xD: ln = 2
            case 0xE:
                if (hb >= 0x0 and hb <= 0x3) or (hb >= 0xC): ln = 2

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
                else: itype = ITYPE.STA
            elif (lb == 0x3 or lb == 0x4 or lb == 0xC): itype = ITYPE.INX
            elif (lb == 0x5 or lb == 0xB or lb == 0xD): itype = ITYPE.DCX
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
                else: itype = ITYPE.LDA
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
            if (lb == 0x2 or lb == 0x3):
                if (hb == 0xC): mod = 4#TODO need to fix
                if (hb == 0xD): itype = ITYPE.OUT
                elif (hb == 0xE): itype = ITYPE.XTHL
                elif (hb == 0xF): itype = ITYPE.DI
                else:
                    itype = ITYPE.JMP
                    mod = hb

        return itype, addrm, mod


    def __init__(self) -> None:
        pass