from enum import Enum


Switch = Enum(
    'Switch', [
        'on_off',           #on off
        'stop_run',         #stop run
        'single_step',      #single step
        'examine',          #examine - examine next
        'deposit',          #deposit - deposit next
        'reset_clr',        #reset clr
        'prtct_unprtct',    #protect - unprotect
        'aux1', 'aux2',     #auxiliary 
        #address switches
        'addr0',
        'addr1',
        'addr2',
        'addr3',
        'addr4',
        'addr5',
        'addr6',
        'addr7',
        'addr8',
        'addr9',
        'addr10',
        'addr11',
        'addr12',
        'addr13',
        'addr14',
        'addr15'
    ]
)

Led = Enum(
    'LED', [
        'power',            #power
        #status
        'inte',             #interrupt
        'prot',             #memory protected
        'memr',             #memory bus read mode
        'inp',              #input device address bus
        'm1',               #is processesing first cycle of instruction
        'out',              #output device address bus
        'hlta',             #halt instruction acknowledged
        'stack',            #stack pointer push down stack address
        'wo',               #write/output instruction
        'int',              #interrupt request acknowledged
        'wait',             #cpu wait state
        'hlda',             #hold acknowledged
        #data at address
        'd0',
        'd1',
        'd2',
        'd3',
        'd4',
        'd5',
        'd6',
        'd7',
        #address
        'a0',
        'a1',
        'a2',
        'a3',
        'a4',
        'a5',
        'a6',
        'a7',
        'a8',
        'a9',
        'a10',
        'a11',
        'a12',
        'a13',
        'a14',
        'a15'
    ]
)

Instr = Enum(
    'Instr', [

    ]
)

#MAX/MINS
MAX16   : int = 512
MAX8    : int = 256
MAX7    : int = 128