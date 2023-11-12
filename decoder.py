from enum import Enum
import os
import re
from config import GetConfig
from inst_info import ADDR_MODE, ITYPE
from util import GetUtil

ADDRM = Enum(
    'ADDRM', [
        'DIR',
        'IMM',
        'REG',
        'IMP'
    ]
)

OPCODE = Enum(
    'OP', [
        'NOP',
        #IO
        'IN', 'OUT',        #IMM

        #Math/Logic
        'ADD', 'SUB',       #IMM, REG
        'ALG',              #Acc Logic
        'DAD',              #REG
        
        #Data Transfer
        'LDA', 'STA',     #IMM, DIR
        'LHLD', 'SHLD',     #DIR
        'SPHL', 'XTHL',     #DIR
        'LXI',
        'MOV',              #IMM, REG

        #Rotate
        'ROT',              #Left/Right/w/wo Carry

        #Comparison
        'CMP',              #IMM, REG

        #Jump
        'JMP',              #IMM, REG 
        'CALL',

        #Return
        'RET',              #IMP, REG

        #Control
        'RST',              #REG
        'HALT',             #IMP

        #Register
        'INR', 'DCR',

        #Flag
        'CRA',              #Carry adjust

        #Accu
        'AAC',              #Accu adjust

        #Stack
        'XCHG',             #DIR
        'POP', 'PUSH',      #REG

        #INTERRUPT
        'INT'               #(Enable/Disable)

    ]
)

class OP:
    name  : str #OP Name
    opcode: OPCODE    #Operand family
    addrm : ADDRM #Address mode
    sz    : int   #Size in bytes
    alt   : int   #Operation mode
    inst  : int  #Raw instruction

    def __init__(self, name:str, inst:int, op:OPCODE, addrm:ADDRM, sz:int, alt:int) -> None:
        self.name = name
        self.inst = inst
        self.op = op
        self.addrm = addrm
        self.sz = sz
        self.alt = alt

class alu_matrix:

    __alu_grid  :[] = []
    __nop       : OP

    def write_grid(self):
        print('    ', end='')
        for lb in range(0x0, 0x10):
            print(f'x{lb:#01x}    '[2:].upper(), end='')
        print('')
        for hb in range(0, 0x10):
            print(f'{hb:#01x}x  '[2:].upper(), end='')
            for lb in range(0, 0x10):
                n = self.get(lb, hb)
                print(f'{n.name:<6}', end='')
            print('')
        print('')
        exit()

    def parse_line(self, ln:str):
        cmnt = ln.find('#')
        if cmnt != -1: ln = ln[:cmnt]
        ln = ln.strip().upper()
        if ln == '': return
        k, v = ln.split(':', 1)
        trms = v.split(',',4)

        fam    = trms[0]
        addrm   = ADDRM[trms[1]]
        sz      = int(trms[2], 0)
        alt     = int(trms[3], 0)
        r       = trms[4][1:len(trms[4])-1].split(',')
        r1      = r[0].split(':')
        r2      = r[1].split(':')
        lb_s    = int(r2[0], 0)
        lb_e    = lb_s
        hb_s    = int(r1[0], 0)
        hb_e    = hb_s     

        if len(r1) == 2: hb_e = int(r1[1], 0)
        if len(r2) == 2: lb_e = int(r2[1], 0)
        
        for l in range(lb_s, lb_e+1): 
            for h in range(hb_s, hb_e+1):
                n = OP(k, (h<<4)|l, OPCODE[fam], addrm, sz, alt)
                self.__alu_grid[l][h] = n
        

    def get(self, lb, hb):
        ret = self.__alu_grid[lb][hb]

        if ret == None: ret = OP('NOP', 0, OPCODE.NOP, 1, 0, 0)
        
        return ret

    def __load_profile(self, profile:str):
        
        util = GetUtil()
        cfg_path = os.path.join(util.cfg_uri, profile)

        for lb in range(0x0, 0x10):
            self.__alu_grid.append([])
            for hb in range(0x0, 0x10):
                self.__alu_grid[lb].append(None)

        f = open(cfg_path, 'r')
        raw = f.readlines()
        f.close()

        for ln in raw:
            self.parse_line(ln)

        self.write_grid()

    def __init__(self, profile:str) -> None:
        self.__load_profile(profile)

class Decoder:

    __matrix : alu_matrix

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
        
        hb = inst >> 0x4
        lb = inst & 0xF
       
        op = self.__matrix.get(lb, hb)

        return OP

    def __init__(self) -> None:
        cfg = GetConfig()
        self.__matrix = alu_matrix(cfg.alu_profile())