from tkinter import IntVar
from defs import *

class __shared_bus:
    
    switches = {}
    leds = {}

    #Methods
    def toggle_led(self, led:Led):
        v = self.leds[led]
        v.set(1 - v.get())

    def toggle_switch(self, switch:Switch):
        v = self.switches[switch]
        b = v.get()
        v.set(1 - v.get())
        a = v.get()
        print('%s -> %s'%(b,a))

    def set_switch(self, switch:Switch, value:int):
        v = self.switches[switch]
        v.set(value)

    def shutoff_display(self):
        for n in self.leds:
            n.set(0)

    def __init__(self):
        for n in Switch:
            self.switches[n.name] = IntVar(value=0)

        for n in Led:
            self.leds[n.name] = IntVar(value=0)

__shared_bus_inst: __shared_bus = None

def SharedState(__shared_bus_inst = __shared_bus_inst) -> __shared_bus:
    if __shared_bus_inst == None:
        __shared_bus_inst = __shared_bus()
    return __shared_bus_inst