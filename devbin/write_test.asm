
LXI H, $P #Load msg ptr to HL
XCHG #Move LH to DE

:loop

LDAX D #Load msg char to acc
OUT $0x0 #Write byte to device
INX D #Inc ptr

CPI 0x0 #Check for end of msg
JZ :loop #Loop

DI
HALT


.data
P $MSG

.bss
MSG "Hello world"
Z 0