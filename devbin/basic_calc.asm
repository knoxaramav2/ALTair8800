EI
#IN      0x0
:START
LDA $op1
MOV B, A
LDA $zero
:LOOP
ADI 0x1
CMP B
JNZ :LOOP
LXI SP, $op2 
HLT

.data
op1    0xFF
op2    0xFF
res    0xFF

.bss
zero   0x0
msg    "Hello World"
