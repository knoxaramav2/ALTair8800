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
        'INX', 'DCX',
        'STA',
        'SHLD', 'LHLD',
        'ROT',
        'CARRY', 'ACCU',
        'MOV',
        'HALT',
        'ADD', 'DAD',
        'SUB',
        'AND', 'OR', 'XOR', 'CMP',
        'RETURN',
        'POP', 'PUSH',
        'JMP', 'CALL',
        'OUT', 'IN', 'XTHL', 'DI'
    ]
)