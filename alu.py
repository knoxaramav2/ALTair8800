
#constants
class Instr:
   #Reference: https://ubuntourist.codeberg.page/Altair-8800/part-4.html
   #IO
   IN       = 0b11011011   #INPUT (byte 2 = device no.)
   OUT      = 0b11010011   #OUTPUT (byte 2 = device no.)

   #INTERR
   EI       = 0b11111011   #ENABLE INTERRUPTS
   DI       = 0b11110011   #DISABLE INTERRUPTS
   HTL      = 0b01110110   #HALT INSTRUCTION
   RST      = 0b11000111   #RESTART INSTRUCTION (bits [4-6] specifies address to continue from as 00 000 000 00 xxx 000)
   #CARRY
   CMC      = 0b00111111   #COMPLIMENT CARRY (update carry bit)
   STC      = 0b00110111   #SET CARRY (update carry bit)

   #NO
   NOP      = 0b00000000   #NO OPERATION

   #USES REGS 000(B), 001(C), 010(D), 100(H), 101(L), 110(M - memory referebce), 111(A)
   #SINGLE REG
   INR      = 0b00000100   #INC REG (bits 4-6 from regs listed) (update zero, sign, parity, aux carry bits)
   DCR      = 0b00000101   #DEC REG ^^^
   CMA      = 0b00101111   #COMPLEMENT ACCU
   DAA      = 0b00100111   #DECIMAL ADJUST ACCU (update zero, sign, parity, carry, aux carry bits)

   #REGS 00(B,C) 01(D,E) 10(H,L) 11(M(flags), A)
   #PAIRED REG
   PUSH     = 0b11000101   #PUSH DATA TO STACK (bits 5-6)
   POP      = 0b11000001   #POP FROM STACK ^^^
   DAD      = 0b00001001   #DOUBLE ADD (update carry bit)
   INX      = 0b00000011   #INC REG PAIR
   DCX      = 0b00001011   #DEC OF ^
   XCHG     = 0b11101011   #EXCHANGE REGS (swap H,L and D,E)
   XTHL     = 0b11100011   #EXCHANGE STACK (LH swapped with stack pointer)
   SPHL     = 0b11111001   #LOAD SP FROM HL
 
   #ROTATE ACCU
   RLC      = 0b00000111   #ROTATE ACCU LEFT (update carry bit)
   RRC      = 0b00001111   #ROTATE ACCU RIGHT (update carry bit)
   RAL      = 0b00010111   #ROTATE ACCU LEFT BY CARRY (update carry bit)
   RAR      = 0b00011111   #ROTATE ACCU RIGHT BY CARRY(update carry bit)

   #REGS 000(B) 001(C) 010(D) 011(E) 100(H) 101(L) 110(M(mem ref)) 111(A(accu))
   #DATA TRANSFER
   MOV      = 0b01000000   #MOVE DATA (move src reg [1-3] to dst reg[4-6]) (src and dest cannot both be 110)
   STAX     = 0b00000010   #STORE ACCU (if bit 4=0, store accu at address in BC, else adddress in DE)
   LDAX     = 0b00001010   #REVERSE OF STAX

   #REGS 000(B) 001(C) 010(D) 011(E) 100(H) 101(L) 110(M(mem ref)) 111(A(accu))
   #REG/MEM TO ACCU
   ADD      = 0b10000000   #ADD REGISTER TO ACCU (reg at bits 1-3) (update carry, sign, zero, aux carry)
   ADC      = 0b10001000   #ADD REGISTER AND CARRY TO ACCU ^^^
   SUB      = 0b10011000   #REVERSE OF ADD
   SBB      = 0b10011000   #REVERSE OF ADC (with borrow)
   ANA      = 0b10100000   #LOGIC AND REG W ACCU(logical AND with reg [1-3] and accu. clear carry) (update carry, zero, sign, parity)
   XRA      = 0b10101000   #LOGIC XOR REG W ACCU ^^^
   ORA      = 0b10110000   #LOGIC OR REG w ACCU ^^^
   CMP      = 0b10111000   #COMPARE REG W ACCU (sub reg from accu) (update carry, sign, zero, parity. sense reversed if diff signs)

   #DIRECT ADDRESSING
   STA      = 0b00110010   #STORE ACCU DIRECT (low addr, high addr)
   LDA      = 0b00110010   #LOAD ACCU DIRECT ^^^
   SHLD     = 0b00100010   #STOR H AND L DIRECT ^^^(L stored in address, H next addr)
   LHLD     = 0b00101010   #LOAD H AND L DIRECT

   #IMMEDIATE
   #REGISTERS 00(BC) 01(DE) 10(HL) 11(SP)
   #REGISTERS 000(B) 001(C) 010(D) 011(E) 100(H) 101(L) 110(M) 111(A)
   LXI      = 0b00000001   #LOAD REG PAIR IMMEDIATE (constants bytes 2,3 loaded to reg at 5-6)
   MVI      = 0b00000110   #MOVE IMMEDIATE DATA ^^^ (only one data byte)
   ADI      = 0b11000110   #ADD IMMEDIATE TO ACCU (add byte 2 to accu) (update carry, sign, zero, parity, aux)
   ACI      = 0b11001110   #ADD IMMEDIATE W CARRY TO ACCU (update carry, sign, zero, parity, aux)
   SUI      = 0b11010110   #SUB IMMEDIATE FROM ACCU ^^
   SBI      = 0b11011110   #SUB IMMEDIATE W CARRY FROM ACCU
   ANI      = 0b11100110   #LOGIC AND IMM WITH ACCU (update carry, sign, zero, parity)
   XRI      = 0b11101110   #LOGIC XOR IMM WITH ACCU ^^^
   ORI      = 0b11110110   #LOGIC OR IMM WITH ACCU ^^^
   CPI      = 0b11111110   #COMPARE IMM WITH ACCU (update carry, zero, sign, parity, aux carry)

   #JUMP
   PCHL     = 0b11101001   #LOAD PROGRAM COUNTER (jump PC to addr in HL)
   JMP      = 0b11000011   #JUMP (jump to address specified by byets 2 and 3)
   JC       = 0b11011010   #JUMP IF CARRY ^^^ (if carry bit set)
   JNC      = 0b11010010   #JUMP IF NO CARRY ^^^
   JZ       = 0b11001010   #JUMP IF ZERO ^^^ (if zero bit set)
   JNZ      = 0b11000010   #JUMP IF NOT ZERO ^^^
   JM       = 0b11111010   #JUMP IF MINUS ^^^(if sign bit set)
   JP       = 0b11110010   #JUMP IF PLUS ^^^ (if sign bit clear)
   JPE      = 0b11101010   #JUMP IF EVEN ^^^ (if parity bit set)
   JPO      = 0b11100010   #JUMP IF ODD ^^^ (if parity bit clear)
   
   #CALL
   CALL     = 0b11001101   #CALL (jump to address specified at bytes 2 and 3)
   CC       = 0b11011100   #CALL IF CARRY ^^^
   CNC      = 0b11010100   #CALL IF NO CARRY ^^^
   CZ       = 0b11001100   #CALL IF ZERO ^^^
   CNZ      = 0b11000100   #CALL IF NOT ZERO ^^^
   CM       = 0b11111100   #CALL IF MINUS ^^^
   CP       = 0b11110100   #CALL IF POSITIVE ^^^
   CPE      = 0b11101100   #CALL IF PARITY EVEN (if parity bit set) ^^^
   CPO      = 0b11100100   #CALL IF PARITY ODD ^^^

   #RETURN
   RET      = 0b11001001   #RETURN (end routine, resume at address on stack)
   RC       = 0b11011000   #RETURN IF CARRY ^^^
   RNC      = 0b11010000   #RETURN IF NO CARRY ^^^
   RZ       = 0b11001000   #RETURN IF ZERO ^^^
   RNZ      = 0b11000000   #RETURN IF NOT ZERO ^^^
   RM       = 0b11111000   #RETURN IF MINUS ^^^
   RP       = 0b11110000   #RETURN IF PLUS ^^^
   RPE      = 0b11101000   #RETURN IF PARITY EVEN ^^^
   RPO      = 0b11100000   #RETURN IF PARITY ODD ^^^


class StatBit:
    CARRY      = 0x1
    AUX_CARRY  = 0x2
    SIGN       = 0x4
    ZERO       = 0x8
    PARITY     = 0x10


class ALU:
    def __init__(self) -> None:
        pass