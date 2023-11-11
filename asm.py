from enum import Enum
import re
from Shared import SharedMachine
from config import GetConfig

Seg = Enum(
    'SEG', [
        'TEXT',
        'DATA',
    ]
)

class ASM:

    #regions
    __start     : int       = 0
    __stack_strt: int       = 0

    # inst, op1, op2
    __text      : [(int, str, str)]     = []
    # label, value
    __data      : dict      = {}
    
    def reg_code1(self, r:str):
        match r:
            case 'B': return 0x0
            case 'C': return 0x1
            case 'D': return 0x2
            case 'E': return 0x3
            case 'H': return 0x4
            case 'L': return 0x5
            case 'M': return 0x6
            case 'SP': return 0x6
            case 'A': return 0x7

    def reg_code2(self, r:str):
        match r:
            case 'B': return 0x0
            case 'D': return 0x1
            case 'E': return 0x2
            case 'PWD': return 0x3
            case 'SP': return 0x3

    def get_data(self, lbl:str):
        return self.__data[lbl]

    def val_to_addr(self, val:str):

        if val.startswith('$'): return val, 0

        tval = int(val, base=0)
        lb = tval & 0x00FF
        hb = tval & 0xFF00
        return lb, hb

    def add_text(self, ln:str):
        trms = re.split(' |,|\t|\n', ln)
        trms = list(filter(None, trms))
        op = trms[0]
        arg1 = trms[1] if len(trms) >= 2 else None
        arg2 = trms[2] if len(trms) >= 3 else None
        inst:  int = 0x0

        match op:
            case 'LDA':  
                inst = 0x3A
                arg1, arg2 = self.val_to_addr(arg1)
            case 'LDAX':
                inst = 0x0A | self.reg_code1(arg1) << 0x4
                arg1 = None
            case 'STA':  
                inst = 0x32
                arg1, arg2 = self.val_to_addr(arg1)
            case 'STAX': 
                inst = 0x02 | (self.reg_code2(arg1) << 0x4) & 0x10
                arg1 = None
            case 'LXI':  
                inst = 0x01 | self.reg_code2(arg1) << 0x4
                arg1, arg2 = self.val_to_addr(arg1)
            case 'INX':
                inst = 0x03 | self.reg_code2(arg1) << 0x4
                arg1 = None
            case 'INR':
                inst = 0x04 | self.reg_code2(arg1) << 0x4
                arg1 = None
            case 'DCR':  
                opr = self.reg_code1(arg1)
                inst = 0x0D if opr & 0x01 else 0x05
                inst |= self.reg_code2(arg1) << 3
            case 'DCX':  
                inst = 0x0B | self.reg_code2(arg1) << 0x4
                arg1 = None
            case 'SHLD': 
                inst = 0x22
                arg1, arg2 = self.val_to_addr(arg1)
            case 'LHLD': 
                inst = 0x2A
                arg1, arg2 = self.val_to_addr(arg1)
            case 'SPHL': inst = 0xF9

            case 'ADD': 
                inst = 0x80  | self.reg_code1(arg1)
                arg1 = None
            case 'ADC': 
                inst = 0x80  | self.reg_code1(arg1) | 0x08
                arg1 = None
            case 'DAD': 
                inst = 0x09  | self.reg_code1(arg1) << 0x4
                arg1 = None
            case 'SUB': 
                inst = 0x90  | self.reg_code1(arg1)
                arg1 = None
            case 'SBB': 
                inst = 0x90  | self.reg_code1(arg1) | 0x08
                arg1 = None

            case 'ANA': 
                inst = 0xA0  | self.reg_code1(arg1)
                arg1 = None
            case 'XRA': 
                inst = 0xA0  | self.reg_code1(arg1) | 0x08
                arg1 = None
            case 'ORA':
                inst = 0xB0  | self.reg_code1(arg1) 
                arg1 = None
            case 'CMP': 
                inst = 0xB0  | self.reg_code1(arg1) | 0x08
                arg1 = None

            case 'RNZ': inst = 0xC0
            case 'RNC': inst = 0xD0
            case 'RPO': inst = 0xE0
            case 'RP':  inst = 0xF0
            case 'RZ':  inst = 0xC8
            case 'RC':  inst = 0xD8
            case 'RPE': inst = 0xE8
            case 'RM':  inst = 0xF8
            case 'RET': inst = 0xC9

            case 'POP': 
                inst = 0xC1  | self.reg_code2(arg1) << 4
                arg1 = None
            case 'PUSH': 
                inst = 0xC5 | self.reg_code2(arg1) << 4
                arg1 = None
            case 'JNZ':
                inst = 0xC2
                arg1, arg2 = self.val_to_addr(arg1)
            case 'JNC':
                inst = 0xD2
                arg1, arg2 = self.val_to_addr(arg1)
            case 'JPO': 
                inst = 0xE2
                arg1, arg2 = self.val_to_addr(arg1)
            case 'JP': 
                inst = 0xF2
                arg1, arg2 = self.val_to_addr(arg1)
            case 'JMP': 
                inst = 0xC3
                arg1, arg2 = self.val_to_addr(arg1)
            case 'JZ':  
                inst = 0xCA
                arg1, arg2 = self.val_to_addr(arg1)
            case 'JC': 
                inst = 0xDA
                arg1, arg2 = self.val_to_addr(arg1)
            case 'JPE':
                inst = 0xEA
                arg1, arg2 = self.val_to_addr(arg1)
            case 'JM': 
                inst = 0xFA
                arg1, arg2 = self.val_to_addr(arg1)

            case 'ADI': inst = 0xC6
            case 'SUI': inst = 0xD6
            case 'ANI': inst = 0xE6
            case 'ORI': inst = 0xF6

            case 'RST': 
                inst = 0xC7 | (0x7 & int(arg1)) << 3
                arg1 = None

            case 'IN':  inst = 0xDB

            case 'XCHG':inst = 0xEB
            case 'EI':  inst = 0xFB

            case 'CZ':  
                inst = 0xCC
                arg1, arg2 = self.val_to_addr(arg1)
            case 'CC':  
                inst = 0xDC
                arg1, arg2 = self.val_to_addr(arg1)
            case 'CPE': 
                inst = 0xEC
                arg1, arg2 = self.val_to_addr(arg1)
            case 'CM':  
                inst = 0xFC
                arg1, arg2 = self.val_to_addr(arg1)
            case 'CALL':
                inst = 0xCD
                arg1, arg2 = self.val_to_addr(arg1)
            case 'CNZ':
                inst = 0xC4
                arg1, arg2 = self.val_to_addr(arg1)
            case 'CNC':
                inst = 0xD4
                arg1, arg2 = self.val_to_addr(arg1)
            case 'CPO':
                inst = 0xE4
                arg1, arg2 = self.val_to_addr(arg1)
            case 'CP':
                inst = 0xF4
                arg1, arg2 = self.val_to_addr(arg1)

            case 'ACI': inst = 0xCE
            case 'SBI': inst = 0xDE
            case 'XRI': inst = 0xEE
            case 'CPI': inst = 0xFE

            case 'MOV':
                inst = 0x40  | self.reg_code1(arg1) << 0x3 | self.reg_code1(arg2)
                arg1 = arg2 = None
            case 'MVI':
                opr = self.reg_code1(arg1)
                inst = 0x0E if opr & 0x01 else 0x06
                inst |= self.reg_code2(arg1) << 3
                arg1 = int(arg2, 0)
                arg2 = None

            case 'RLC': inst = 0x07
            case 'RAL': inst = 0x17
            case 'DAA': inst = 0x27
            case 'STC': inst = 0x37
            case 'RRC': inst = 0x0F
            case 'RAR': inst = 0x1F
            case 'CMA': inst = 0x2F
            case 'CMC': inst = 0x3F

            case "HLT": inst = 0x76

            case _: print(f'WRN: Unknown instruction {op}')

        self.__text.append((inst, arg1, arg2))

    def add_data(self, ln:str):
        k, v = ln.split()
        self.__data[k] = v

    def get_sym_loc(self, val, offset):
        if not isinstance(val, str):
            return f'0o{val:03o}' if val != None else None
        val = val.removeprefix('$')
        t = 0xFF
        if  self.__data.get(val): t = list(self.__data.keys()).index(val)
        else:
            print(f'Unrecognized symbol \'{val}\'')

        return f'0o{(t+offset):03o}'

    def translate(self):
        ret = []
        err = False
        
        cfg = GetConfig()
        #stack_sz = cfg.stack_size()
        data_sz = len(self.__data)
        inst_sz = 0

        #find inst size
        for i in self.__text:
            inst_sz += (
                1 if i[1] == None else
                2 if i[2] == None else 3)

        res_size = inst_sz+data_sz+1
        ret = ['000'] * (res_size)
        ret[0] = 'base=8'

        #set data region
        offs = inst_sz
        i = 1
        for k,v in self.__data.items():
            #TODO pre write calcs
            ret[offs + i] = f'0o{int(v,8):03o}'
            i += 1

        i = 1
        for inst in self.__text:
            ret[i] = f'0o{inst[0]:03o}'
            a1 = self.get_sym_loc(inst[1], inst_sz)
            a2 = self.get_sym_loc(inst[2], inst_sz)

            if (a1 == None and inst[1] != None or 
                a2 == None and inst[2] != None): 
                err = True
                break

            if a1 != None: 
                i+=1
                ret[i] = a1
            if a2 != None: 
                i+=1
                ret[i] = a2

            i += 1

        if err: return None

        return ret

    def load(self, file:str):
        f = open(file, 'r')
        lns = f.readlines()
        f.close()

        seg = Seg.TEXT
        err = False
        parr = []

        print(f'ASSEMBLIING \'{file}\'')
        for ln in lns:
            #Normalize line
            cidx = ln.find('#')
            if cidx != -1: ln = ln[0:cidx]
            ln = ln.strip().upper()
            if str.isspace(ln) or ln=='': continue

            if ln.startswith(('.', '_')):
                match ln:
                    case '.TEXT': seg = Seg.TEXT
                    case '.DATA': seg = Seg.DATA
                    case '_START': pass
                    case _: print(f'WRN: Unknown section or region \'{ln}\'')
                continue
            
            match seg:
                case Seg.TEXT:  self.add_text(ln)
                case Seg.DATA:  self.add_data(ln)
        
        if err: return

        res = self.translate()

        if res == None:
            print('Assembly failed')
            return

        file = file.replace('.asm', '.prg')
        f = open(file, 'w')
        for i in range(0, len(res)):
            f.write(res[i]+'\n')
        f.close()

    def __init__(self) -> None:
        pass