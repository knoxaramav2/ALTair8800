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

_clr_power = 'white'
_clr_ctrl = 'cyan'
_clr_aux = 'black'
_clr_a8_15 = 'red'
_clr_a7_0 = 'white'

def SwitchColor(x : Switch):
    return {
        Switch.on_off : _clr_power,

        Switch.stop_run : _clr_ctrl,
        Switch.single_step : _clr_ctrl,
        Switch.examine : _clr_ctrl,
        Switch.deposit : _clr_ctrl,
        Switch.reset_clr : _clr_ctrl,
        Switch.prtct_unprtct : _clr_ctrl,

        Switch.aux1 : _clr_aux,
        Switch.aux2 : _clr_aux,

        Switch.addr0 : _clr_a7_0,
        Switch.addr1 : _clr_a7_0,
        Switch.addr2 : _clr_a7_0,
        Switch.addr3 : _clr_a7_0,
        Switch.addr4 : _clr_a7_0,
        Switch.addr5 : _clr_a7_0,
        Switch.addr6 : _clr_a7_0,
        Switch.addr7 : _clr_a7_0,

        Switch.addr8 : _clr_a8_15,
        Switch.addr9 : _clr_a8_15,
        Switch.addr10 : _clr_a8_15,
        Switch.addr11 : _clr_a8_15,
        Switch.addr12 : _clr_a8_15,
        Switch.addr13 : _clr_a8_15,
        Switch.addr14 : _clr_a8_15,
        Switch.addr15 : _clr_a8_15,
    }.get(x)

def LedColor(x : Led):
    return 'red'