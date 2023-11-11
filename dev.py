

import os
from Shared import SharedCPU, SharedMachine
from asm import ASM
from config import GetConfig
from util import GetUtil


def load_program(cmp:SharedMachine):

    file = GetConfig().program_file().lower()
    util = GetUtil()
    base_uri = util.base_uri+'\\devbin'

    if os.path.isfile(file) == False:
        file = os.path.join(base_uri, file)
        if os.path.isfile(file) == False:
            f'Cannot open \'{file}\''
            return
    
    cmp.reset()

    if file.endswith('.asm'): load_asm(cmp, file)
    file = file.replace('.asm', '.prg')
    load_prg(cmp, file)
    

def load_prg(cmp:SharedMachine, file:str):
    
    util = GetUtil()
    cpu = cmp.get_cpu()

    base     = 0

    f = open(file, 'r')
    lns = f.readlines()

    if len(lns) == 0: return

    bstr = lns[0]
    if bstr.startswith('base'):
        bval = bstr.split('=')[1]
        base = int(bval)
        lns.pop(0)

    parr = []
    i = 0
    for ln in lns:
        #Normalize line
        i += 1
        ln = ln.strip()
        if str.isspace(ln) or ln=='': continue
        cidx = ln.find('#')
        if cidx != -1: ln = ln[0:cidx]
        if len(ln) >=2 and ln[1].isalpha(): ln = ln[2:]
        if not ln.replace(' ', '').isnumeric():
            if not ln.startswith('.'):
                print(f'Invalid PRG CODE: {i}: {ln}')
                continue
            else:
                parr.append(ln)
                continue
        parr.extend(ln.split())

    for nstr in parr:
        if not nstr.isnumeric():
            k, v = nstr.split(' ')
            match k:
                case '.offset': cpu.set_addr(int(v, base))
                case _: print('Unknown label ' + nstr)
            continue
        
        num = nstr
        if isinstance(nstr, str):
            num = int(nstr, base)

        for i in range(0, 8):
            sw = num & (1 << i)
            cmp.data_buffer[i].set(sw)
        cpu.set_word(util.boolarr_to_int(cmp.data_buffer)&0xFF)
        cpu.next_addr()
    
    cmp.reset()

    print(f'LOADED {file}:')
    for p in parr:
        print(p)

def load_asm(cmp:SharedMachine, file:str):
    asm:ASM = ASM()
    asm.load(file)