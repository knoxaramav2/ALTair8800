from Controls import *
from Shared import *

def stop_run(host, ctrl:Ctrl):
    if ctrl.state.get() == 1:#STOP
        ctrl.var = False
    else:#RUN
        ctrl.var = True
    if ctrl.var: print('RUN') 
    else: print('STOP')

def next_step(host, ctrl:Ctrl):    
    host.s_cpu.next_addr()
    print('STEP ' + ctrl.upper_text + ' ' + str(host.s_cpu.inst_ptr))

def examine(host, ctrl:Ctrl):
    print('Examine')
    if ctrl.state.get() == 0:#EXAMINE NEXT
        host.s_cpu.next_addr()
    host.s_cmp.set_cpu_addr()
    host.s_cpu.update_data_buffer()
    print("EXAM. %s at %s"%(host.s_cpu.get_curr_data(), host.s_cpu.inst_ptr))

def deposit(host, ctrl:Ctrl):
    print('Deposit')
    if ctrl.state.get() == 0:#DEPOSIT NEXT
        host.s_cpu.next_addr()
    host.s_cpu.set_word(host.s_cmp.get_sw_addr()&0xFF)

def reset(host, ctrl:Ctrl):
    print('Reset')
    if ctrl.state.get() == 1:#REST
        pass
    else:#CLR
        pass

def protect(host, ctrl:Ctrl):
    print('Protect')
    if ctrl.state.get() == 1:#PROTECT
        pass
    else:#UNPROTECT
        pass

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
    print('CLICK CTRL')
    ctrl.base.configure(image=ctrl.imgs[0])
    ctrl.base.after(100, lambda:ctrl.base.configure(image=ctrl.imgs[1]))

    if next_fnc != None:
        next_fnc()

def toggle_addr(ctrl:CtrlSwitch):
    print('TOGGLE ADDR %s'%ctrl.var.get())

def toggle_power(ctrl:CtrlSwitch, scmp:SharedMachine):
    b = scmp.power_on.get()
    print('TOGGLE POWER : %s'%b)
