from chip8080 import GetChip8080


def cycle_led_regs():

    chip = GetChip8080()
    chip.mem.stack_set(3, 92)#Should trigger 0101 1100

    print('DEV: SET STAT LIGHTS')