

import os
from Shared import SharedCPU, SharedMachine
from config import GetConfig
from util import GetUtil


def load_program(cmp:SharedMachine):
    file = GetConfig().program_file()
    util = GetUtil()
    base_uri = util.base_uri+'\\devbin'

    if os.path.isfile(file) == False:
        file = os.path.join(base_uri, file)
        if os.path.isfile(file) == False:
            f'Cannot open \'{file}\''
            return
    
    cmp.reset()

    base = 0
    f = open(file, 'r')
    lns = f.readlines()

    bstr = lns[0]
    if bstr.startswith('base'):
        bval = bstr.split('=')[1]
        base = int(bval)
        lns.pop(0)

    parr = []
    for ln in lns:
        ln = ln.strip()
        if str.isspace(ln) or ln=='': continue
        cidx = ln.find('#')
        if cidx != -1: ln = ln[0:cidx]
        parr.extend(ln.split())

    for nstr in parr:
        num = int(nstr, base)

        for i in range(0, 8):
            sw = num & (1 << i)
            cmp.addr_sw[i].set(sw)
        cmp.cpu.set_word(cmp.get_sw_addr()&0xFF)
        cmp.cpu.next_addr()
    cmp.reset()

    print(f'LOADED {file}:')
    for p in parr:
        print(p)