from inst_info import ADDR_MODE, ITYPE

class Decoder:
    
    def inst_len(inst:int):
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

    def decode_inst(inst:int) -> [ITYPE, ADDR_MODE]:
        
        addrm   : ADDR_MODE = None
        type    : ITYPE = None

        return type, addrm


    def __init__(self) -> None:
        pass