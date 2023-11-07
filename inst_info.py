from enum import Enum

ADDR_MODE = Enum(
    'addr_mode',[
        'IMM'
    ]
)

ITYPE = Enum(
    'itype',[
        'LDAX',
        'STAX',

        'MOV',

        'ADD',

        'JMP'
    ]
)