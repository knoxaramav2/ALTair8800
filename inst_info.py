from enum import Enum

ADDR_MODE = Enum(
    'addr_mode',[
        'IMPLIED',
        'REGISTER',
        'IMMEDIATE',
        'DIRECT'
    ]
)

ITYPE = Enum(
    'itype',[
        'NOP',
        'LDA', 'LXI',
        'SHLD', 'LHLD', 'SPHL',
        'INX', 'DCX',
        'STA',
        'ROT',
        'CARRY', 'ACCU',
        'MOV', 'XCHG',
        'HALT',
        'ADD', 'DAD',
        'SUB',
        'AND', 'OR', 'XOR', 'CMP',
        'RETURN',
        'POP', 'PUSH',
        'JMP', 'CALL',
        'OUT', 'IN', 'XTHL', 'DI',
        'INT',
        'RESET'
    ]
)