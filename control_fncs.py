
from Controls import *
from Shared import SharedMachine

def stop_run(host, ctrl:Ctrl):
    if ctrl.state.get() == 1:#STOP
        host.s_cu.halt()
    else:#RUN
        host.s_cu.start()
    if ctrl.var: print('RUN') 
    else: print('STOP')

def next_step(host, ctrl:Ctrl):
    host.s_cu.step()
    host.s_cmp.update_addr_buffer()

def examine(host, ctrl:Ctrl):
    print('Examine')
    if ctrl.state.get() == 0:#EXAMINE NEXT
        host.s_cpu.next_addr()
        host.s_cmp.update_addr_buffer()
    else:
        host.s_cmp.set_cpu_addr()
    host.s_cpu.update_data_buffer()
    print("EXAM. %s at %s"%(host.s_cpu.read_mem(), host.s_cpu.inst_ptr))

def deposit(host, ctrl:Ctrl):
    print('Deposit')
    if ctrl.state.get() == 0:#DEPOSIT NEXT
        host.s_cpu.next_addr()
        host.s_cmp.update_addr_buffer()
    host.s_cpu.set_word(host.s_cmp.get_sw_addr()&0xFF)

def reset(host, ctrl:Ctrl):
    print('Reset')
    if ctrl.state.get() == 1:#RESET
        host.s_cmp.reset()
    else:#CLR
        pass

def protect(host, ctrl:Ctrl):
    print('Protect')
    if ctrl.state.get() == 1:#PROTECT
        host.s_mem.protect.set(True)
    else:#UNPROTECT
        host.s_mem.protect.set(False)

def toggle_ctrl(ctrl:CtrlSwitch, next_fnc=None):
    print('TOGGLE CTRL')
    y = ctrl.base.winfo_pointery()
    yc = ctrl.base.winfo_y()
    yr = ctrl.base.master.winfo_rooty()
    h = ctrl.base.winfo_height()
    up = (y - (yr + yc)) < (h/2)

    if up:
        ctrl.state.set(1)
        ctrl.base.configure(image=ctrl.imgs[2])
    else:
        ctrl.state.set(0)
        ctrl.base.configure(image=ctrl.imgs[0])
    ctrl.base.after(200, lambda:ctrl.base.configure(image=ctrl.imgs[1]))

    if next_fnc != None:
        next_fnc()

def click_ctrl(ctrl:CtrlButton, next_fnc=None):
    ctrl.base.configure(image=ctrl.imgs[0])
    ctrl.base.after(100, lambda:ctrl.base.configure(image=ctrl.imgs[1]))

    if next_fnc != None:
        next_fnc()

def toggle_addr(ctrl:CtrlSwitch):
    print('TOGGLE ADDR %s'%ctrl.var.get())

def toggle_power(ctrl:CtrlSwitch, scmp:SharedMachine):
    b = scmp.power_on.get()
    print('TOGGLE POWER : %s'%b)
