lda $T1
mov d, a
lda $T2
add d
stax B
lda $T3
ldax B
jmp 0x0
.data
T1 4
T2 3
T3 66