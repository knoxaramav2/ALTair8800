

def cycle_led_regs(cmp):

    print('DEV: SET STAT LIGHTS')

    #Set 
    cmp.mem.set_heap(20, 92)
    cmp.cpu.ip_set(20)


