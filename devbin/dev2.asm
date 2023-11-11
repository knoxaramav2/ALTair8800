
#ASSEMBLY TEST SCRIPT

#define code segment==========================
#code is the default segment and can be omitted if first
.text

#define starting point========================
#must be within code segment
#defaults as first code line if omitted
_start      
LDA     0x80    #Load immediate
MOV     B, A
LDA     $arg2   #Load from data section
MOV     C, A
LDA     $arg1   #Load from data section
ADD     B
SUB     C
STA     $result
JMP     0x00
HLT

#define static data labels====================
.data
arg1    0xA
arg2    0x21
result  0xFF

#define variable data labels==================
#.bss


