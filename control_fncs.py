from Controls import *
from Shared import *


def toggle_ctrl(ctrl:CtrlSwitch):
    print('TOGGLE CTRL')
    y = ctrl.base.winfo_pointery()
    yc = ctrl.base.winfo_y()
    yr = ctrl.base.master.winfo_rooty()
    h = ctrl.base.winfo_height()
    n = y - (yr + yc)
    if n < h/2:
        ctrl.base.configure(image=ctrl.imgs[2])
    else:
        ctrl.base.configure(image=ctrl.imgs[0])
    ctrl.base.after(200, lambda:ctrl.base.configure(image=ctrl.imgs[1]))

def click_ctrl(ctrl:CtrlButton):
    print('CLICK CTRL')
    ctrl.base.configure(image=ctrl.imgs[0])
    ctrl.base.after(100, lambda:ctrl.base.configure(image=ctrl.imgs[1]))

def toggle_addr(ctrl:CtrlSwitch):
    print('TOGGLE ADDR')

def toggle_power(ctrl:CtrlSwitch, scmp:SharedMachine):
    b = scmp.power_on.get()
    print('TOGGLE POWER : %s'%b)
